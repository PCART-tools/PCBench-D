    def _slice(self, slobj: slice, axis: int = 0) -> Series:
        # axis kwarg is retained for compat with NDFrame method
        #  _slice is *always* positional
        return self._get_values(slobj)
