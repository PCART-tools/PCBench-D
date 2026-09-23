    def _seek(self, frame: int, update_image: bool = True) -> None:
        if isinstance(self._fp, DeferredError):
            raise self._fp.ex
        if frame == 0:
            # rewind
            self.__offset = 0
            self.dispose: _imaging.ImagingCore | None = None
            self.__frame = -1
            self._fp.seek(self.__rewind)
            self.disposal_method = 0
            if "comment" in self.info:
                del self.info["comment"]
        else:
            # ensure that the previous frame was loaded
            if self.tile and update_image:
                self.load()

        if frame != self.__frame + 1:
            msg = f"cannot seek to frame {frame}"
            raise ValueError(msg)

        self.fp = self._fp
        if self.__offset:
            # backup to last frame
            self.fp.seek(self.__offset)
            while self.data():
                pass
            self.__offset = 0

        s = self.fp.read(1)
        if not s or s == b";":
            msg = "no more images in GIF file"
            raise EOFError(msg)

        palette: ImagePalette.ImagePalette | Literal[False] | None = None

        info: dict[str, Any] = {}
        frame_transparency = None
        interlace = None
        frame_dispose_extent = None
        while True:
            if not s:
                s = self.fp.read(1)
            if not s or s == b";":
                break

            elif s == b"!":
                #
                # extensions
                #
                s = self.fp.read(1)
                block = self.data()
                if s[0] == 249 and block is not None:
                    #
                    # graphic control extension
                    #
                    flags = block[0]
                    if flags & 1:
                        frame_transparency = block[3]
                    info["duration"] = i16(block, 1) * 10

                    # disposal method - find the value of bits 4 - 6
                    dispose_bits = 0b00011100 & flags
                    dispose_bits = dispose_bits >> 2
                    if dispose_bits:
                        # only set the dispose if it is not
                        # unspecified. I'm not sure if this is
                        # correct, but it seems to prevent the last
                        # frame from looking odd for some animations
                        self.disposal_method = dispose_bits
                elif s[0] == 254:
                    #
                    # comment extension
                    #
                    comment = b""

                    # Read this comment block
                    while block:
                        comment += block
                        block = self.data()

                    if "comment" in info:
                        # If multiple comment blocks in frame, separate with \n
                        info["comment"] += b"\n" + comment
                    else:
                        info["comment"] = comment
                    s = None
                    continue
                elif s[0] == 255 and frame == 0 and block is not None:
                    #
                    # application extension
                    #
                    info["extension"] = block, self.fp.tell()
                    if block.startswith(b"NETSCAPE2.0"):
                        block = self.data()
                        if block and len(block) >= 3 and block[0] == 1:
                            self.info["loop"] = i16(block, 1)
                while self.data():
                    pass

            elif s == b",":
                #
                # local image
                #
                s = self.fp.read(9)

                # extent
                x0, y0 = i16(s, 0), i16(s, 2)
                x1, y1 = x0 + i16(s, 4), y0 + i16(s, 6)
                if (x1 > self.size[0] or y1 > self.size[1]) and update_image:
                    self._size = max(x1, self.size[0]), max(y1, self.size[1])
                    Image._decompression_bomb_check(self._size)
                frame_dispose_extent = x0, y0, x1, y1
                flags = s[8]

                interlace = (flags & 64) != 0

                if flags & 128:
                    bits = (flags & 7) + 1
                    p = self.fp.read(3 << bits)
                    if self._is_palette_needed(p):
                        palette = ImagePalette.raw("RGB", p)
                    else:
                        palette = False

                # image data
                bits = self.fp.read(1)[0]
                self.__offset = self.fp.tell()
                break
            s = None

        if interlace is None:
            msg = "image not found in GIF frame"
            raise EOFError(msg)

        self.__frame = frame
        if not update_image:
            return

        self.tile = []

        if self.dispose:
            self.im.paste(self.dispose, self.dispose_extent)

        self._frame_palette = palette if palette is not None else self.global_palette
        self._frame_transparency = frame_transparency
        if frame == 0:
            if self._frame_palette:
                if LOADING_STRATEGY == LoadingStrategy.RGB_ALWAYS:
                    self._mode = "RGBA" if frame_transparency is not None else "RGB"
                else:
                    self._mode = "P"
            else:
                self._mode = "L"

            if palette:
                self.palette = palette
            elif self.global_palette:
                from copy import copy

                self.palette = copy(self.global_palette)
            else:
                self.palette = None
        else:
            if self.mode == "P":
                if (
                    LOADING_STRATEGY != LoadingStrategy.RGB_AFTER_DIFFERENT_PALETTE_ONLY
                    or palette
                ):
                    if "transparency" in self.info:
                        self.im.putpalettealpha(self.info["transparency"], 0)
                        self.im = self.im.convert("RGBA", Image.Dither.FLOYDSTEINBERG)
                        self._mode = "RGBA"
                        del self.info["transparency"]
                    else:
                        self._mode = "RGB"
                        self.im = self.im.convert("RGB", Image.Dither.FLOYDSTEINBERG)

        def _rgb(color: int) -> tuple[int, int, int]:
            if self._frame_palette:
                if color * 3 + 3 > len(self._frame_palette.palette):
                    color = 0
                return tuple(self._frame_palette.palette[color * 3 : color * 3 + 3])
            else:
                return (color, color, color)

        self.dispose = None
        self.dispose_extent = frame_dispose_extent
        if self.dispose_extent and self.disposal_method >= 2:
            try:
                if self.disposal_method == 2:
                    # replace with background colour

                    # only dispose the extent in this frame
                    x0, y0, x1, y1 = self.dispose_extent
                    dispose_size = (x1 - x0, y1 - y0)

                    Image._decompression_bomb_check(dispose_size)

                    # by convention, attempt to use transparency first
                    dispose_mode = "P"
                    color = self.info.get("transparency", frame_transparency)
                    if color is not None:
                        if self.mode in ("RGB", "RGBA"):
                            dispose_mode = "RGBA"
                            color = _rgb(color) + (0,)
                    else:
                        color = self.info.get("background", 0)
                        if self.mode in ("RGB", "RGBA"):
                            dispose_mode = "RGB"
                            color = _rgb(color)
                    self.dispose = Image.core.fill(dispose_mode, dispose_size, color)
                else:
                    # replace with previous contents
                    if self._im is not None:
                        # only dispose the extent in this frame
                        self.dispose = self._crop(self.im, self.dispose_extent)
                    elif frame_transparency is not None:
                        x0, y0, x1, y1 = self.dispose_extent
                        dispose_size = (x1 - x0, y1 - y0)

                        Image._decompression_bomb_check(dispose_size)
                        dispose_mode = "P"
                        color = frame_transparency
                        if self.mode in ("RGB", "RGBA"):
                            dispose_mode = "RGBA"
                            color = _rgb(frame_transparency) + (0,)
                        self.dispose = Image.core.fill(
                            dispose_mode, dispose_size, color
                        )
            except AttributeError:
                pass

        if interlace is not None:
            transparency = -1
            if frame_transparency is not None:
                if frame == 0:
                    if LOADING_STRATEGY != LoadingStrategy.RGB_ALWAYS:
                        self.info["transparency"] = frame_transparency
                elif self.mode not in ("RGB", "RGBA"):
                    transparency = frame_transparency
            self.tile = [
                ImageFile._Tile(
                    "gif",
                    (x0, y0, x1, y1),
                    self.__offset,
                    (bits, interlace, transparency),
                )
            ]

        if info.get("comment"):
            self.info["comment"] = info["comment"]
        for k in ["duration", "extension"]:
            if k in info:
                self.info[k] = info[k]
            elif k in self.info:
                del self.info[k]
