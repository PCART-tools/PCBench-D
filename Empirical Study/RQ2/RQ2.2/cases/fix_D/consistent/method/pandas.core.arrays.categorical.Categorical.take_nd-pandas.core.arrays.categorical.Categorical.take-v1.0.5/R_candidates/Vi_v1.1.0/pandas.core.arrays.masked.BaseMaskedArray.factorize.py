    @doc(ExtensionArray.factorize)
    def factorize(self, na_sentinel: int = -1) -> Tuple[np.ndarray, ExtensionArray]:
        arr = self._data
        mask = self._mask

        codes, uniques = _factorize_array(arr, na_sentinel=na_sentinel, mask=mask)

        # the hashtables don't handle all different types of bits
        uniques = uniques.astype(self.dtype.numpy_dtype, copy=False)
        uniques = type(self)(uniques, np.zeros(len(uniques), dtype=bool))
        return codes, uniques
