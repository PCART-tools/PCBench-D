    def __str__(self):
        return "{}({!r})".format(type(self).__name__,
            "clip" if self._clip else "mask")
