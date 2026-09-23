    def _try_coerce_args(self, values, other):
        """ provide coercion to our input arguments
            we are going to compare vs i8, so coerce to floats
            repring NaT with np.nan so nans propagate
            values is always ndarray like, other may not be """
        def masker(v):
            mask = isnull(v)
            v = v.view('i8').astype('float64')
            v[mask] = np.nan
            return v

        values = masker(values)

        if is_null_datelike_scalar(other):
            other = np.nan
        elif isinstance(other, (np.timedelta64, Timedelta, timedelta)):
            other = _coerce_scalar_to_timedelta_type(other, unit='s', box=False).item()
            if other == tslib.iNaT:
                other = np.nan
        else:
            other = masker(other)

        return values, other
