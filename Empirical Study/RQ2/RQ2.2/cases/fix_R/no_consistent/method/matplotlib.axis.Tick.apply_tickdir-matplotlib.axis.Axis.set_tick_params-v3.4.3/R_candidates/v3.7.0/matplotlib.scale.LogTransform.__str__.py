    def __str__(self):
        return "{}(base={}, nonpositive={!r})".format(
            type(self).__name__, self.base, "clip" if self._clip else "mask")
