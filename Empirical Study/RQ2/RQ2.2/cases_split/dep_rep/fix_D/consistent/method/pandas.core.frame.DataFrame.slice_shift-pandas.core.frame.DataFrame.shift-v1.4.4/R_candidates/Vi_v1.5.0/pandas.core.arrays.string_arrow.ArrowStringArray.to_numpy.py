    def to_numpy(
        self,
        dtype: npt.DTypeLike | None = None,
        copy: bool = False,
        na_value=lib.no_default,
    ) -> np.ndarray:
        """
        Convert to a NumPy ndarray.
        """
        # TODO: copy argument is ignored

        result = np.array(self._data, dtype=dtype)
        if self._data.null_count > 0:
            if na_value is lib.no_default:
                if dtype and np.issubdtype(dtype, np.floating):
                    return result
                na_value = self._dtype.na_value
            mask = self.isna()
            result[mask] = na_value
        return result
