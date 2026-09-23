    def __str__(self):
        return "{}(base={}, nonpos={!r})".format(
            type(self).__name__, self.base, "clip" if self._clip else "mask")
