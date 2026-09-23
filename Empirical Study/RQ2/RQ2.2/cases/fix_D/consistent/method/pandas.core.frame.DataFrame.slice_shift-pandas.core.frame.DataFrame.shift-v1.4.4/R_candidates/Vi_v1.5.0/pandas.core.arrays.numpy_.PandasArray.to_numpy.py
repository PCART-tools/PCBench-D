    def to_numpy(
        self,
        dtype: npt.DTypeLike | None = None,
        copy: bool = False,
        na_value: object = lib.no_default,
    ) -> np.ndarray:
        result = np.asarray(self._ndarray, dtype=dtype)

        if (copy or na_value is not lib.no_default) and result is self._ndarray:
            result = result.copy()

        if na_value is not lib.no_default:
            result[self.isna()] = na_value

        return result
