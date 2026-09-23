    def _quantile(
        self: NDArrayBackedExtensionArrayT,
        qs: npt.NDArray[np.float64],
        interpolation: str,
    ) -> NDArrayBackedExtensionArrayT:
        # TODO: disable for Categorical if not ordered?

        mask = np.asarray(self.isna())
        arr = self._ndarray
        fill_value = self._internal_fill_value

        res_values = quantile_with_mask(arr, mask, fill_value, qs, interpolation)

        res_values = self._cast_quantile_result(res_values)
        return self._from_backing_data(res_values)
