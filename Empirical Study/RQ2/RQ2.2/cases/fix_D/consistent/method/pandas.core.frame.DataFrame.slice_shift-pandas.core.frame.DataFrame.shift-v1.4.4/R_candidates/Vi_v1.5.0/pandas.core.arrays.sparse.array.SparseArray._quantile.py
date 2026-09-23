    def _quantile(self, qs: npt.NDArray[np.float64], interpolation: str):

        if self._null_fill_value or self.sp_index.ngaps == 0:
            # We can avoid densifying
            npvalues = self.sp_values
            mask = np.zeros(npvalues.shape, dtype=bool)
        else:
            npvalues = self.to_numpy()
            mask = self.isna()

        fill_value = na_value_for_dtype(npvalues.dtype, compat=False)
        res_values = quantile_with_mask(
            npvalues,
            mask,
            fill_value,
            qs,
            interpolation,
        )

        # Special case: the returned array isn't _really_ sparse, so we don't
        #  wrap it in a SparseArray
        return res_values
