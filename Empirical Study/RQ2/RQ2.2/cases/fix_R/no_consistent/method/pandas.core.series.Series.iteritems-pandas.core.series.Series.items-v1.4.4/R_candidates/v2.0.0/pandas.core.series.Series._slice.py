    def _slice(self, slobj: slice | np.ndarray, axis: Axis = 0) -> Series:
        # axis kwarg is retained for compat with NDFrame method
        #  _slice is *always* positional
        return self._get_values(slobj)
