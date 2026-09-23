    def _cast_quantile_result(self, res_values: np.ndarray) -> np.ndarray:
        """
        Cast the result of quantile_with_mask to an appropriate dtype
        to pass to _from_backing_data in _quantile.
        """
        return res_values
