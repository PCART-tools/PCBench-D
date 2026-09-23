    def load_prepare(self) -> None:
        temp_mode = "P" if self._frame_palette else "L"
        self._prev_im = None
        if self.__frame == 0:
            if self._frame_transparency is not None:
                self.im = Image.core.fill(
                    temp_mode, self.size, self._frame_transparency
                )
        elif self.mode in ("RGB", "RGBA"):
            self._prev_im = self.im
            if self._frame_palette:
                self.im = Image.core.fill("P", self.size, self._frame_transparency or 0)
                self.im.putpalette("RGB", *self._frame_palette.getdata())
            else:
                self._im = None
        if not self._prev_im and self._im is not None and self.size != self.im.size:
            expanded_im = Image.core.fill(self.im.mode, self.size)
            if self._frame_palette:
                expanded_im.putpalette("RGB", *self._frame_palette.getdata())
            expanded_im.paste(self.im, (0, 0) + self.im.size)

            self.im = expanded_im
        self._mode = temp_mode
        self._frame_palette = None

        super().load_prepare()
