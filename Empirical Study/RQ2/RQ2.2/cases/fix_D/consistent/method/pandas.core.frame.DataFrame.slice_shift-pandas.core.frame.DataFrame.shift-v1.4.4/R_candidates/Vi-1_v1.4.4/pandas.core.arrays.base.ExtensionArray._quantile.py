    def _quantile(
        self: ExtensionArrayT, qs: npt.NDArray[np.float64], interpolation: str
    ) -> ExtensionArrayT:
        """
        Compute the quantiles of self for each quantile in `qs`.

        Parameters
        ----------
        qs : np.ndarray[float64]
        interpolation: str

        Returns
        -------
        same type as self
        """
        # asarray needed for Sparse, see GH#24600
        mask = np.asarray(self.isna())
        mask = np.atleast_2d(mask)

        arr = np.atleast_2d(np.asarray(self))
        fill_value = np.nan

        res_values = quantile_with_mask(arr, mask, fill_value, qs, interpolation)

        if self.ndim == 2:
            # i.e. DatetimeArray
            result = type(self)._from_sequence(res_values)

        else:
            # shape[0] should be 1 as long as EAs are 1D
            assert res_values.shape == (1, len(qs)), res_values.shape
            result = type(self)._from_sequence(res_values[0])

        return result
