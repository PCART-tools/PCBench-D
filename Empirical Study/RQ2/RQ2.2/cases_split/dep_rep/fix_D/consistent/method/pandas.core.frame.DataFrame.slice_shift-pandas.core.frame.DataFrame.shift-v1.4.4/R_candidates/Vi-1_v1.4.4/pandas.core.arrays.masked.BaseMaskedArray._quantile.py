    def _quantile(
        self: BaseMaskedArrayT, qs: npt.NDArray[np.float64], interpolation: str
    ) -> BaseMaskedArrayT:
        """
        Dispatch to quantile_with_mask, needed because we do not have
        _from_factorized.

        Notes
        -----
        We assume that all impacted cases are 1D-only.
        """
        mask = np.atleast_2d(np.asarray(self.isna()))
        npvalues: np.ndarray = np.atleast_2d(np.asarray(self))

        res = quantile_with_mask(
            npvalues,
            mask=mask,
            fill_value=self.dtype.na_value,
            qs=qs,
            interpolation=interpolation,
        )
        assert res.ndim == 2
        assert res.shape[0] == 1
        res = res[0]
        try:
            out = type(self)._from_sequence(res, dtype=self.dtype)
        except TypeError:
            # GH#42626: not able to safely cast Int64
            # for floating point output
            out = np.asarray(res, dtype=np.float64)
        return out
