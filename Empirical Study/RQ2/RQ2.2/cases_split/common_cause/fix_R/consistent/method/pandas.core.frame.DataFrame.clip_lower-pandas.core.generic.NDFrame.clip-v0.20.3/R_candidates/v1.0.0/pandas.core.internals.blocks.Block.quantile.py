    def quantile(self, qs, interpolation="linear", axis=0):
        """
        compute the quantiles of the

        Parameters
        ----------
        qs: a scalar or list of the quantiles to be computed
        interpolation: type of interpolation, default 'linear'
        axis: axis to compute, default 0

        Returns
        -------
        Block
        """
        # We should always have ndim == 2 because Series dispatches to DataFrame
        assert self.ndim == 2

        values = self.get_values()

        is_empty = values.shape[axis] == 0
        orig_scalar = not is_list_like(qs)
        if orig_scalar:
            # make list-like, unpack later
            qs = [qs]

        if is_empty:
            # create the array of na_values
            # 2d len(values) * len(qs)
            result = np.repeat(
                np.array([self.fill_value] * len(qs)), len(values)
            ).reshape(len(values), len(qs))
        else:
            # asarray needed for Sparse, see GH#24600
            mask = np.asarray(isna(values))
            result = nanpercentile(
                values,
                np.array(qs) * 100,
                axis=axis,
                na_value=self.fill_value,
                mask=mask,
                ndim=values.ndim,
                interpolation=interpolation,
            )

            result = np.array(result, copy=False)
            result = result.T

        if orig_scalar and not lib.is_scalar(result):
            # result could be scalar in case with is_empty and self.ndim == 1
            assert result.shape[-1] == 1, result.shape
            result = result[..., 0]
            result = lib.item_from_zerodim(result)

        ndim = np.ndim(result)
        return make_block(result, placement=np.arange(len(result)), ndim=ndim)
