    def _open(self):
        if not _accept(self.fp.read(4)):
            msg = "not a DDS file"
            raise SyntaxError(msg)
        (header_size,) = struct.unpack("<I", self.fp.read(4))
        if header_size != 124:
            msg = f"Unsupported header size {repr(header_size)}"
            raise OSError(msg)
        header_bytes = self.fp.read(header_size - 4)
        if len(header_bytes) != 120:
            msg = f"Incomplete header: {len(header_bytes)} bytes"
            raise OSError(msg)
        header = BytesIO(header_bytes)

        flags, height, width = struct.unpack("<3I", header.read(12))
        self._size = (width, height)
        self._mode = "RGBA"

        pitch, depth, mipmaps = struct.unpack("<3I", header.read(12))
        struct.unpack("<11I", header.read(44))  # reserved

        # pixel format
        pfsize, pfflags = struct.unpack("<2I", header.read(8))
        fourcc = header.read(4)
        (bitcount,) = struct.unpack("<I", header.read(4))
        masks = struct.unpack("<4I", header.read(16))
        if pfflags & DDPF_LUMINANCE:
            # Texture contains uncompressed L or LA data
            if pfflags & DDPF_ALPHAPIXELS:
                self._mode = "LA"
            else:
                self._mode = "L"

            self.tile = [("raw", (0, 0) + self.size, 0, (self.mode, 0, 1))]
        elif pfflags & DDPF_RGB:
            # Texture contains uncompressed RGB data
            masks = {mask: ["R", "G", "B", "A"][i] for i, mask in enumerate(masks)}
            rawmode = ""
            if pfflags & DDPF_ALPHAPIXELS:
                rawmode += masks[0xFF000000]
            else:
                self._mode = "RGB"
            rawmode += masks[0xFF0000] + masks[0xFF00] + masks[0xFF]

            self.tile = [("raw", (0, 0) + self.size, 0, (rawmode[::-1], 0, 1))]
        elif pfflags & DDPF_PALETTEINDEXED8:
            self._mode = "P"
            self.palette = ImagePalette.raw("RGBA", self.fp.read(1024))
            self.tile = [("raw", (0, 0) + self.size, 0, "L")]
        else:
            data_start = header_size + 4
            n = 0
            if fourcc == b"DXT1":
                self.pixel_format = "DXT1"
                n = 1
            elif fourcc == b"DXT3":
                self.pixel_format = "DXT3"
                n = 2
            elif fourcc == b"DXT5":
                self.pixel_format = "DXT5"
                n = 3
            elif fourcc == b"ATI1":
                self.pixel_format = "BC4"
                n = 4
                self._mode = "L"
            elif fourcc in (b"ATI2", b"BC5U"):
                self.pixel_format = "BC5"
                n = 5
                self._mode = "RGB"
            elif fourcc == b"BC5S":
                self.pixel_format = "BC5S"
                n = 5
                self._mode = "RGB"
            elif fourcc == b"DX10":
                data_start += 20
                # ignoring flags which pertain to volume textures and cubemaps
                (dxgi_format,) = struct.unpack("<I", self.fp.read(4))
                self.fp.read(16)
                if dxgi_format in (DXGI_FORMAT_BC5_TYPELESS, DXGI_FORMAT_BC5_UNORM):
                    self.pixel_format = "BC5"
                    n = 5
                    self._mode = "RGB"
                elif dxgi_format == DXGI_FORMAT_BC5_SNORM:
                    self.pixel_format = "BC5S"
                    n = 5
                    self._mode = "RGB"
                elif dxgi_format == DXGI_FORMAT_BC6H_UF16:
                    self.pixel_format = "BC6H"
                    n = 6
                    self._mode = "RGB"
                elif dxgi_format == DXGI_FORMAT_BC6H_SF16:
                    self.pixel_format = "BC6HS"
                    n = 6
                    self._mode = "RGB"
                elif dxgi_format in (DXGI_FORMAT_BC7_TYPELESS, DXGI_FORMAT_BC7_UNORM):
                    self.pixel_format = "BC7"
                    n = 7
                elif dxgi_format == DXGI_FORMAT_BC7_UNORM_SRGB:
                    self.pixel_format = "BC7"
                    self.info["gamma"] = 1 / 2.2
                    n = 7
                elif dxgi_format in (
                    DXGI_FORMAT_R8G8B8A8_TYPELESS,
                    DXGI_FORMAT_R8G8B8A8_UNORM,
                    DXGI_FORMAT_R8G8B8A8_UNORM_SRGB,
                ):
                    self.tile = [("raw", (0, 0) + self.size, 0, ("RGBA", 0, 1))]
                    if dxgi_format == DXGI_FORMAT_R8G8B8A8_UNORM_SRGB:
                        self.info["gamma"] = 1 / 2.2
                    return
                else:
                    msg = f"Unimplemented DXGI format {dxgi_format}"
                    raise NotImplementedError(msg)
            else:
                msg = f"Unimplemented pixel format {repr(fourcc)}"
                raise NotImplementedError(msg)

            self.tile = [
                ("bcn", (0, 0) + self.size, data_start, (n, self.pixel_format))
            ]
