    def load_end(self) -> None:
        """internal: finished reading image data"""
        assert self.png is not None
        if self.__idat != 0:
            self.fp.read(self.__idat)
        while True:
            self.fp.read(4)  # CRC

            try:
                cid, pos, length = self.png.read()
            except (struct.error, SyntaxError):
                break

            if cid == b"IEND":
                break
            elif cid == b"fcTL" and self.is_animated:
                # start of the next frame, stop reading
                self.__prepare_idat = 0
                self.png.push(cid, pos, length)
                break

            try:
                self.png.call(cid, pos, length)
            except UnicodeDecodeError:
                break
            except EOFError:
                if cid == b"fdAT":
                    length -= 4
                try:
                    ImageFile._safe_read(self.fp, length)
                except OSError as e:
                    if ImageFile.LOAD_TRUNCATED_IMAGES:
                        break
                    else:
                        raise e
            except AttributeError:
                logger.debug("%r %s %s (unknown)", cid, pos, length)
                s = ImageFile._safe_read(self.fp, length)
                if cid[1:2].islower():
                    self.private_chunks.append((cid, s, True))
        self._text = self.png.im_text
        if not self.is_animated:
            self.png.close()
            self.png = None
        else:
            if self._prev_im and self.blend_op == Blend.OP_OVER:
                updated = self._crop(self.im, self.dispose_extent)
                if self.im.mode == "RGB" and "transparency" in self.info:
                    mask = updated.convert_transparent(
                        "RGBA", self.info["transparency"]
                    )
                else:
                    if self.im.mode == "P" and "transparency" in self.info:
                        t = self.info["transparency"]
                        if isinstance(t, bytes):
                            updated.putpalettealphas(t)
                        elif isinstance(t, int):
                            updated.putpalettealpha(t)
                    mask = updated.convert("RGBA")
                self._prev_im.paste(updated, self.dispose_extent, mask)
                self.im = self._prev_im
