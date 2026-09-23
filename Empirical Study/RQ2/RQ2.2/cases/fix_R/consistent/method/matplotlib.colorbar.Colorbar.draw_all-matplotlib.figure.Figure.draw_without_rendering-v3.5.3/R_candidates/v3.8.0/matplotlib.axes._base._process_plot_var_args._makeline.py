    def _makeline(self, axes, x, y, kw, kwargs):
        kw = {**kw, **kwargs}  # Don't modify the original kw.
        default_dict = self._getdefaults(set(), kw)
        self._setdefaults(default_dict, kw)
        seg = mlines.Line2D(x, y, **kw)
        return seg, kw
