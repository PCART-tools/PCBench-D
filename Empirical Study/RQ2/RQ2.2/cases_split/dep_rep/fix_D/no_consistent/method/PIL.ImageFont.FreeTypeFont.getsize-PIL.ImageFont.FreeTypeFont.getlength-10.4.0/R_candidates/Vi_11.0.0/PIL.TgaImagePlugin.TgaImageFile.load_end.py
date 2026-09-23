    def load_end(self) -> None:
        if self._flip_horizontally:
            self.im = self.im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
