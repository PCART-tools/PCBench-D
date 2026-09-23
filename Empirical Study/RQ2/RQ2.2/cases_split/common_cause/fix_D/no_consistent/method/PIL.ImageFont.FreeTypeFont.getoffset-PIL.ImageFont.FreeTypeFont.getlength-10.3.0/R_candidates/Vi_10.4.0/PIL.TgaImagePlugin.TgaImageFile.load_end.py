    def load_end(self) -> None:
        if self._flip_horizontally:
            assert self.im is not None
            self.im = self.im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
