    def _try_coerce_args(self, values, other):
        """ Coerce values and other to float64, with null values converted to
            NaN. values is always ndarray-like, other may not be """
        def masker(v):
            mask = isnull(v)
            v = v.astype('float64')
            v[mask] = np.nan
            return v

        values = masker(values)

        if is_null_datelike_scalar(other):
            other = np.nan
        elif isinstance(other, (np.timedelta64, Timedelta, timedelta)):
            other = _coerce_scalar_to_timedelta_type(other, unit='s', box=False).item()
            if other == tslib.iNaT:
                other = np.nan
        elif lib.isscalar(other):
            other = np.float64(other)
        else:
            other = masker(other)

        return values, other
