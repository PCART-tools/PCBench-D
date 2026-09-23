    def _bitmap(self, header: int = 0, offset: int = 0) -> None:
        """Read relevant info about the BMP"""
        read, seek = self.fp.read, self.fp.seek
        if header:
            seek(header)
        # read bmp header size @offset 14 (this is part of the header size)
        file_info: dict[str, bool | int | tuple[int, ...]] = {
            "header_size": i32(read(4)),
            "direction": -1,
        }

        # -------------------- If requested, read header at a specific position
        # read the rest of the bmp header, without its size
        assert isinstance(file_info["header_size"], int)
        header_data = ImageFile._safe_read(self.fp, file_info["header_size"] - 4)

        # ------------------------------- Windows Bitmap v2, IBM OS/2 Bitmap v1
        # ----- This format has different offsets because of width/height types
        # 12: BITMAPCOREHEADER/OS21XBITMAPHEADER
        if file_info["header_size"] == 12:
            file_info["width"] = i16(header_data, 0)
            file_info["height"] = i16(header_data, 2)
            file_info["planes"] = i16(header_data, 4)
            file_info["bits"] = i16(header_data, 6)
            file_info["compression"] = self.COMPRESSIONS["RAW"]
            file_info["palette_padding"] = 3

        # --------------------------------------------- Windows Bitmap v3 to v5
        #  40: BITMAPINFOHEADER
        #  52: BITMAPV2HEADER
        #  56: BITMAPV3HEADER
        #  64: BITMAPCOREHEADER2/OS22XBITMAPHEADER
        # 108: BITMAPV4HEADER
        # 124: BITMAPV5HEADER
        elif file_info["header_size"] in (40, 52, 56, 64, 108, 124):
            file_info["y_flip"] = header_data[7] == 0xFF
            file_info["direction"] = 1 if file_info["y_flip"] else -1
            file_info["width"] = i32(header_data, 0)
            file_info["height"] = (
                i32(header_data, 4)
                if not file_info["y_flip"]
                else 2**32 - i32(header_data, 4)
            )
            file_info["planes"] = i16(header_data, 8)
            file_info["bits"] = i16(header_data, 10)
            file_info["compression"] = i32(header_data, 12)
            # byte size of pixel data
            file_info["data_size"] = i32(header_data, 16)
            file_info["pixels_per_meter"] = (
                i32(header_data, 20),
                i32(header_data, 24),
            )
            file_info["colors"] = i32(header_data, 28)
            file_info["palette_padding"] = 4
            assert isinstance(file_info["pixels_per_meter"], tuple)
            self.info["dpi"] = tuple(x / 39.3701 for x in file_info["pixels_per_meter"])
            if file_info["compression"] == self.COMPRESSIONS["BITFIELDS"]:
                masks = ["r_mask", "g_mask", "b_mask"]
                if len(header_data) >= 48:
                    if len(header_data) >= 52:
                        masks.append("a_mask")
                    else:
                        file_info["a_mask"] = 0x0
                    for idx, mask in enumerate(masks):
                        file_info[mask] = i32(header_data, 36 + idx * 4)
                else:
                    # 40 byte headers only have the three components in the
                    # bitfields masks, ref:
                    # https://msdn.microsoft.com/en-us/library/windows/desktop/dd183376(v=vs.85).aspx
                    # See also
                    # https://github.com/python-pillow/Pillow/issues/1293
                    # There is a 4th component in the RGBQuad, in the alpha
                    # location, but it is listed as a reserved component,
                    # and it is not generally an alpha channel
                    file_info["a_mask"] = 0x0
                    for mask in masks:
                        file_info[mask] = i32(read(4))
                assert isinstance(file_info["r_mask"], int)
                assert isinstance(file_info["g_mask"], int)
                assert isinstance(file_info["b_mask"], int)
                assert isinstance(file_info["a_mask"], int)
                file_info["rgb_mask"] = (
                    file_info["r_mask"],
                    file_info["g_mask"],
                    file_info["b_mask"],
                )
                file_info["rgba_mask"] = (
                    file_info["r_mask"],
                    file_info["g_mask"],
                    file_info["b_mask"],
                    file_info["a_mask"],
                )
        else:
            msg = f"Unsupported BMP header type ({file_info['header_size']})"
            raise OSError(msg)

        # ------------------ Special case : header is reported 40, which
        # ---------------------- is shorter than real size for bpp >= 16
        assert isinstance(file_info["width"], int)
        assert isinstance(file_info["height"], int)
        self._size = file_info["width"], file_info["height"]

        # ------- If color count was not found in the header, compute from bits
        assert isinstance(file_info["bits"], int)
        file_info["colors"] = (
            file_info["colors"]
            if file_info.get("colors", 0)
            else (1 << file_info["bits"])
        )
        assert isinstance(file_info["colors"], int)
        if offset == 14 + file_info["header_size"] and file_info["bits"] <= 8:
            offset += 4 * file_info["colors"]

        # ---------------------- Check bit depth for unusual unsupported values
        self._mode, raw_mode = BIT2MODE.get(file_info["bits"], ("", ""))
        if not self.mode:
            msg = f"Unsupported BMP pixel depth ({file_info['bits']})"
            raise OSError(msg)

        # ---------------- Process BMP with Bitfields compression (not palette)
        decoder_name = "raw"
        if file_info["compression"] == self.COMPRESSIONS["BITFIELDS"]:
            SUPPORTED: dict[int, list[tuple[int, ...]]] = {
                32: [
                    (0xFF0000, 0xFF00, 0xFF, 0x0),
                    (0xFF000000, 0xFF0000, 0xFF00, 0x0),
                    (0xFF000000, 0xFF00, 0xFF, 0x0),
                    (0xFF000000, 0xFF0000, 0xFF00, 0xFF),
                    (0xFF, 0xFF00, 0xFF0000, 0xFF000000),
                    (0xFF0000, 0xFF00, 0xFF, 0xFF000000),
                    (0xFF000000, 0xFF00, 0xFF, 0xFF0000),
                    (0x0, 0x0, 0x0, 0x0),
                ],
                24: [(0xFF0000, 0xFF00, 0xFF)],
                16: [(0xF800, 0x7E0, 0x1F), (0x7C00, 0x3E0, 0x1F)],
            }
            MASK_MODES = {
                (32, (0xFF0000, 0xFF00, 0xFF, 0x0)): "BGRX",
                (32, (0xFF000000, 0xFF0000, 0xFF00, 0x0)): "XBGR",
                (32, (0xFF000000, 0xFF00, 0xFF, 0x0)): "BGXR",
                (32, (0xFF000000, 0xFF0000, 0xFF00, 0xFF)): "ABGR",
                (32, (0xFF, 0xFF00, 0xFF0000, 0xFF000000)): "RGBA",
                (32, (0xFF0000, 0xFF00, 0xFF, 0xFF000000)): "BGRA",
                (32, (0xFF000000, 0xFF00, 0xFF, 0xFF0000)): "BGAR",
                (32, (0x0, 0x0, 0x0, 0x0)): "BGRA",
                (24, (0xFF0000, 0xFF00, 0xFF)): "BGR",
                (16, (0xF800, 0x7E0, 0x1F)): "BGR;16",
                (16, (0x7C00, 0x3E0, 0x1F)): "BGR;15",
            }
            if file_info["bits"] in SUPPORTED:
                if (
                    file_info["bits"] == 32
                    and file_info["rgba_mask"] in SUPPORTED[file_info["bits"]]
                ):
                    assert isinstance(file_info["rgba_mask"], tuple)
                    raw_mode = MASK_MODES[(file_info["bits"], file_info["rgba_mask"])]
                    self._mode = "RGBA" if "A" in raw_mode else self.mode
                elif (
                    file_info["bits"] in (24, 16)
                    and file_info["rgb_mask"] in SUPPORTED[file_info["bits"]]
                ):
                    assert isinstance(file_info["rgb_mask"], tuple)
                    raw_mode = MASK_MODES[(file_info["bits"], file_info["rgb_mask"])]
                else:
                    msg = "Unsupported BMP bitfields layout"
                    raise OSError(msg)
            else:
                msg = "Unsupported BMP bitfields layout"
                raise OSError(msg)
        elif file_info["compression"] == self.COMPRESSIONS["RAW"]:
            if file_info["bits"] == 32 and header == 22:  # 32-bit .cur offset
                raw_mode, self._mode = "BGRA", "RGBA"
        elif file_info["compression"] in (
            self.COMPRESSIONS["RLE8"],
            self.COMPRESSIONS["RLE4"],
        ):
            decoder_name = "bmp_rle"
        else:
            msg = f"Unsupported BMP compression ({file_info['compression']})"
            raise OSError(msg)

        # --------------- Once the header is processed, process the palette/LUT
        if self.mode == "P":  # Paletted for 1, 4 and 8 bit images
            # ---------------------------------------------------- 1-bit images
            if not (0 < file_info["colors"] <= 65536):
                msg = f"Unsupported BMP Palette size ({file_info['colors']})"
                raise OSError(msg)
            else:
                assert isinstance(file_info["palette_padding"], int)
                padding = file_info["palette_padding"]
                palette = read(padding * file_info["colors"])
                grayscale = True
                indices = (
                    (0, 255)
                    if file_info["colors"] == 2
                    else list(range(file_info["colors"]))
                )

                # ----------------- Check if grayscale and ignore palette if so
                for ind, val in enumerate(indices):
                    rgb = palette[ind * padding : ind * padding + 3]
                    if rgb != o8(val) * 3:
                        grayscale = False

                # ------- If all colors are gray, white or black, ditch palette
                if grayscale:
                    self._mode = "1" if file_info["colors"] == 2 else "L"
                    raw_mode = self.mode
                else:
                    self._mode = "P"
                    self.palette = ImagePalette.raw(
                        "BGRX" if padding == 4 else "BGR", palette
                    )

        # ---------------------------- Finally set the tile data for the plugin
        self.info["compression"] = file_info["compression"]
        args: list[Any] = [raw_mode]
        if decoder_name == "bmp_rle":
            args.append(file_info["compression"] == self.COMPRESSIONS["RLE4"])
        else:
            assert isinstance(file_info["width"], int)
            args.append(((file_info["width"] * file_info["bits"] + 31) >> 3) & (~3))
        args.append(file_info["direction"])
        self.tile = [
            ImageFile._Tile(
                decoder_name,
                (0, 0, file_info["width"], file_info["height"]),
                offset or self.fp.tell(),
                tuple(args),
            )
        ]
