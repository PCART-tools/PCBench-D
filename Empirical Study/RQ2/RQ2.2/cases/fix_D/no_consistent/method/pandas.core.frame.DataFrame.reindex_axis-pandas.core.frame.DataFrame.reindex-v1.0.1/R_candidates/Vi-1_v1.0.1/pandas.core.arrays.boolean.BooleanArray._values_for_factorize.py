    def _values_for_factorize(self) -> Tuple[np.ndarray, Any]:
        data = self._data.astype("int8")
        data[self._mask] = -1
        return data, -1
