    def _make_line(self, axes, x, y, kw, kwargs):
        kw = {**kw, **kwargs}  # Don't modify the original kw.
        self._setdefaults(self._getdefaults(kw), kw)
        seg = mlines.Line2D(x, y, **kw)
        return seg, kw
