    def _seek(self, frame: int, rewind: bool = False) -> None:
        assert self.png is not None

        self.dispose: _imaging.ImagingCore | None
        dispose_extent = None
        if frame == 0:
            if rewind:
                self._fp.seek(self.__rewind)
                self.png.rewind()
                self.__prepare_idat = self.__rewind_idat
                self._im = None
                self.info = self.png.im_info
                self.tile = self.png.im_tile
                self.fp = self._fp
            self._prev_im = None
            self.dispose = None
            self.default_image = self.info.get("default_image", False)
            self.dispose_op = self.info.get("disposal")
            self.blend_op = self.info.get("blend")
            dispose_extent = self.info.get("bbox")
            self.__frame = 0
        else:
            if frame != self.__frame + 1:
                msg = f"cannot seek to frame {frame}"
                raise ValueError(msg)

            # ensure previous frame was loaded
            self.load()

            if self.dispose:
                self.im.paste(self.dispose, self.dispose_extent)
            self._prev_im = self.im.copy()

            self.fp = self._fp

            # advance to the next frame
            if self.__prepare_idat:
                ImageFile._safe_read(self.fp, self.__prepare_idat)
                self.__prepare_idat = 0
            frame_start = False
            while True:
                self.fp.read(4)  # CRC

                try:
                    cid, pos, length = self.png.read()
                except (struct.error, SyntaxError):
                    break

                if cid == b"IEND":
                    msg = "No more images in APNG file"
                    raise EOFError(msg)
                if cid == b"fcTL":
                    if frame_start:
                        # there must be at least one fdAT chunk between fcTL chunks
                        msg = "APNG missing frame data"
                        raise SyntaxError(msg)
                    frame_start = True

                try:
                    self.png.call(cid, pos, length)
                except UnicodeDecodeError:
                    break
                except EOFError:
                    if cid == b"fdAT":
                        length -= 4
                        if frame_start:
                            self.__prepare_idat = length
                            break
                    ImageFile._safe_read(self.fp, length)
                except AttributeError:
                    logger.debug("%r %s %s (unknown)", cid, pos, length)
                    ImageFile._safe_read(self.fp, length)

            self.__frame = frame
            self.tile = self.png.im_tile
            self.dispose_op = self.info.get("disposal")
            self.blend_op = self.info.get("blend")
            dispose_extent = self.info.get("bbox")

            if not self.tile:
                msg = "image not found in APNG frame"
                raise EOFError(msg)
        if dispose_extent:
            self.dispose_extent: tuple[float, float, float, float] = dispose_extent

        # setup frame disposal (actual disposal done when needed in the next _seek())
        if self._prev_im is None and self.dispose_op == Disposal.OP_PREVIOUS:
            self.dispose_op = Disposal.OP_BACKGROUND

        self.dispose = None
        if self.dispose_op == Disposal.OP_PREVIOUS:
            if self._prev_im:
                self.dispose = self._prev_im.copy()
                self.dispose = self._crop(self.dispose, self.dispose_extent)
        elif self.dispose_op == Disposal.OP_BACKGROUND:
            self.dispose = Image.core.fill(self.mode, self.size)
            self.dispose = self._crop(self.dispose, self.dispose_extent)
