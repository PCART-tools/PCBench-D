    def _slice(self, slobj: slice, axis: AxisInt = 0) -> Series:
        # axis kwarg is retained for compat with NDFrame method
        #  _slice is *always* positional
        mgr = self._mgr.get_slice(slobj, axis=axis)
        out = self._constructor(mgr, fastpath=True)
        return out.__finalize__(self)
