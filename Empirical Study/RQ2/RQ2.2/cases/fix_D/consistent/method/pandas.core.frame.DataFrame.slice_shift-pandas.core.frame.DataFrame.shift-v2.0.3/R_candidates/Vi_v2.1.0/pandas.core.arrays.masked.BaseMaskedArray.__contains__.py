    def __contains__(self, key) -> bool:
        if isna(key) and key is not self.dtype.na_value:
            # GH#52840
            if self._data.dtype.kind == "f" and lib.is_float(key):
                return bool((np.isnan(self._data) & ~self._mask).any())

        return bool(super().__contains__(key))
