    def load_prepare(self):
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
                self.im.putpalette(*self._frame_palette.getdata())
            else:
                self.im = None
        self.mode = temp_mode
        self._frame_palette = None

        super().load_prepare()
