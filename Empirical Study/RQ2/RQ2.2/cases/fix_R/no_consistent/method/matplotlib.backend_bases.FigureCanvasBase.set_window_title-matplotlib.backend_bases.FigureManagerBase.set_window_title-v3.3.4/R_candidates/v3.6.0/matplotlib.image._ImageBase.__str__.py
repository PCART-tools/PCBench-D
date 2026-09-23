    def __str__(self):
        try:
            size = self.get_size()
            return f"{type(self).__name__}(size={size!r})"
        except RuntimeError:
            return type(self).__name__
