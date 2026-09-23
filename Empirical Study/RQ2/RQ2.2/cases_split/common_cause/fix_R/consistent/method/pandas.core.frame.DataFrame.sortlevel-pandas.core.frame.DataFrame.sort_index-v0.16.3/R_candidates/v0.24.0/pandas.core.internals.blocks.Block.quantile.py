    def quantile(self, qs, interpolation='linear', axis=0):
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
        if self.is_datetimetz:
            # TODO: cleanup this special case.
            # We need to operate on i8 values for datetimetz
            # but `Block.get_values()` returns an ndarray of objects
            # right now. We need an API for "values to do numeric-like ops on"
            values = self.values.asi8

            # TODO: NonConsolidatableMixin shape
            # Usual shape inconsistencies for ExtensionBlocks
            if self.ndim > 1:
                values = values[None, :]
        else:
            values = self.get_values()
            values, _ = self._try_coerce_args(values, values)

        is_empty = values.shape[axis] == 0
        orig_scalar = not is_list_like(qs)
        if orig_scalar:
            # make list-like, unpack later
            qs = [qs]

        if is_empty:
            if self.ndim == 1:
                result = self._na_value
            else:
                # create the array of na_values
                # 2d len(values) * len(qs)
                result = np.repeat(np.array([self.fill_value] * len(qs)),
                                   len(values)).reshape(len(values),
                                                        len(qs))
        else:
            # asarray needed for Sparse, see GH#24600
            # TODO: Why self.values and not values?
            mask = np.asarray(isna(self.values))
            result = nanpercentile(values, np.array(qs) * 100,
                                   axis=axis, na_value=self.fill_value,
                                   mask=mask, ndim=self.ndim,
                                   interpolation=interpolation)

            result = np.array(result, copy=False)
            if self.ndim > 1:
                result = result.T

        if orig_scalar and not lib.is_scalar(result):
            # result could be scalar in case with is_empty and self.ndim == 1
            assert result.shape[-1] == 1, result.shape
            result = result[..., 0]
            result = lib.item_from_zerodim(result)

        ndim = getattr(result, 'ndim', None) or 0
        result = self._try_coerce_result(result)
        return make_block(result,
                          placement=np.arange(len(result)),
                          ndim=ndim)
