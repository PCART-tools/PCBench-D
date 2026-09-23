    def translated(self, tx, ty):
        """Construct a `Bbox` by translating this one by *tx* and *ty*."""
        return Bbox(self._points + (tx, ty))
