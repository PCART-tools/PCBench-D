    def _quantile(
        self: NDArrayBackedExtensionArrayT,
        qs: npt.NDArray[np.float64],
        interpolation: str,
    ) -> NDArrayBackedExtensionArrayT:
        # TODO: disable for Categorical if not ordered?

        # asarray needed for Sparse, see GH#24600
        mask = np.asarray(self.isna())
        mask = np.atleast_2d(mask)

        arr = np.atleast_2d(self._ndarray)
        # TODO: something NDArrayBacked-specific instead of _values_for_factorize[1]?
        fill_value = self._values_for_factorize()[1]

        res_values = quantile_with_mask(arr, mask, fill_value, qs, interpolation)

        result = type(self)._from_factorized(res_values, self)
        if self.ndim == 1:
            assert result.shape == (1, len(qs)), result.shape
            result = result[0]

        return result
