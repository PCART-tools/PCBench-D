    def _cast_quantile_result(self, res_values: np.ndarray) -> np.ndarray:
        # make sure we have correct itemsize for resulting codes
        assert res_values.dtype == self._ndarray.dtype
        return res_values
