    def quantile(self, qs, interpolation='linear', axis=0, mgr=None):
        """
        compute the quantiles of the

        Parameters
        ----------
        qs: a scalar or list of the quantiles to be computed
        interpolation: type of interpolation, default 'linear'
        axis: axis to compute, default 0

        Returns
        -------
        tuple of (axis, block)

        """
        if _np_version_under1p9:
            if interpolation != 'linear':
                raise ValueError("Interpolation methods other than linear "
                                 "are not supported in numpy < 1.9.")

        kw = {}
        if not _np_version_under1p9:
            kw.update({'interpolation': interpolation})

        values = self.get_values()
        values, _, _, _ = self._try_coerce_args(values, values)

        def _nanpercentile1D(values, mask, q, **kw):
            values = values[~mask]

            if len(values) == 0:
                if is_scalar(q):
                    return self._na_value
                else:
                    return np.array([self._na_value] * len(q),
                                    dtype=values.dtype)

            return np.percentile(values, q, **kw)

        def _nanpercentile(values, q, axis, **kw):

            mask = isnull(self.values)
            if not is_scalar(mask) and mask.any():
                if self.ndim == 1:
                    return _nanpercentile1D(values, mask, q, **kw)
                else:
                    # for nonconsolidatable blocks mask is 1D, but values 2D
                    if mask.ndim < values.ndim:
                        mask = mask.reshape(values.shape)
                    if axis == 0:
                        values = values.T
                        mask = mask.T
                    result = [_nanpercentile1D(val, m, q, **kw) for (val, m)
                              in zip(list(values), list(mask))]
                    result = np.array(result, dtype=values.dtype, copy=False).T
                    return result
            else:
                return np.percentile(values, q, axis=axis, **kw)

        from pandas import Float64Index
        is_empty = values.shape[axis] == 0
        if is_list_like(qs):
            ax = Float64Index(qs)

            if is_empty:
                if self.ndim == 1:
                    result = self._na_value
                else:
                    # create the array of na_values
                    # 2d len(values) * len(qs)
                    result = np.repeat(np.array([self._na_value] * len(qs)),
                                       len(values)).reshape(len(values),
                                                            len(qs))
            else:

                try:
                    result = _nanpercentile(values, np.array(qs) * 100,
                                            axis=axis, **kw)
                except ValueError:

                    # older numpies don't handle an array for q
                    result = [_nanpercentile(values, q * 100,
                                             axis=axis, **kw) for q in qs]

                result = np.array(result, copy=False)
                if self.ndim > 1:
                    result = result.T

        else:

            if self.ndim == 1:
                ax = Float64Index([qs])
            else:
                ax = mgr.axes[0]

            if is_empty:
                if self.ndim == 1:
                    result = self._na_value
                else:
                    result = np.array([self._na_value] * len(self))
            else:
                result = _nanpercentile(values, qs * 100, axis=axis, **kw)

        ndim = getattr(result, 'ndim', None) or 0
        result = self._try_coerce_result(result)
        if is_scalar(result):
            return ax, self.make_block_scalar(result)
        return ax, make_block(result,
                              placement=np.arange(len(result)),
                              ndim=ndim)
