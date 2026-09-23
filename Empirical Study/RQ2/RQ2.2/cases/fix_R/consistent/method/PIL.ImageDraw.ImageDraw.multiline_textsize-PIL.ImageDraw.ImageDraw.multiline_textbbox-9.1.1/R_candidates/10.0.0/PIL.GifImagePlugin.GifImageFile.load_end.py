    def load_end(self):
        if self.__frame == 0:
            if self.mode == "P" and LOADING_STRATEGY == LoadingStrategy.RGB_ALWAYS:
                if self._frame_transparency is not None:
                    self.im.putpalettealpha(self._frame_transparency, 0)
                    self.mode = "RGBA"
                else:
                    self.mode = "RGB"
                self.im = self.im.convert(self.mode, Image.Dither.FLOYDSTEINBERG)
            return
        if not self._prev_im:
            return
        if self._frame_transparency is not None:
            self.im.putpalettealpha(self._frame_transparency, 0)
            frame_im = self.im.convert("RGBA")
        else:
            frame_im = self.im.convert("RGB")
        frame_im = self._crop(frame_im, self.dispose_extent)

        self.im = self._prev_im
        self.mode = self.im.mode
        if frame_im.mode == "RGBA":
            self.im.paste(frame_im, self.dispose_extent, frame_im)
        else:
            self.im.paste(frame_im, self.dispose_extent)
