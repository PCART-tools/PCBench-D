    def _quantile(
        self, qs: npt.NDArray[np.float64], interpolation: str
    ) -> BaseMaskedArray:
        """
        Dispatch to quantile_with_mask, needed because we do not have
        _from_factorized.

        Notes
        -----
        We assume that all impacted cases are 1D-only.
        """
        res = quantile_with_mask(
            self._data,
            mask=self._mask,
            # TODO(GH#40932): na_value_for_dtype(self.dtype.numpy_dtype)
            #  instead of np.nan
            fill_value=np.nan,
            qs=qs,
            interpolation=interpolation,
        )

        if self._hasna:
            # Our result mask is all-False unless we are all-NA, in which
            #  case it is all-True.
            if self.ndim == 2:
                # I think this should be out_mask=self.isna().all(axis=1)
                #  but am holding off until we have tests
                raise NotImplementedError
            elif self.isna().all():
                out_mask = np.ones(res.shape, dtype=bool)
            else:
                out_mask = np.zeros(res.shape, dtype=bool)
        else:
            out_mask = np.zeros(res.shape, dtype=bool)
        return self._maybe_mask_result(res, mask=out_mask)
