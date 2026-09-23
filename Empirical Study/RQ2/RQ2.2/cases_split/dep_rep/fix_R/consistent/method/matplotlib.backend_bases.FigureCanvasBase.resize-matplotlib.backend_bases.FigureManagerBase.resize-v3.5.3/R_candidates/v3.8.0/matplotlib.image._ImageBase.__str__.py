    def __str__(self):
        try:
            shape = self.get_shape()
            return f"{type(self).__name__}(shape={shape!r})"
        except RuntimeError:
            return type(self).__name__
