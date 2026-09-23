    def _make_coordinates(self, axes, x, y, kw, kwargs):
        kw = {**kw, **kwargs}  # Don't modify the original kw.
        self._setdefaults(self._getdefaults(kw), kw)
        return (x, y), kw
