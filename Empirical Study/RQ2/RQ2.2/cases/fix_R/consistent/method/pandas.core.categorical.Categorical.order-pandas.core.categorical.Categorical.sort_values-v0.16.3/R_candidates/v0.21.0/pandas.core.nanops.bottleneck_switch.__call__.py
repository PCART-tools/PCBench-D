    def __call__(self, alt):
        bn_name = alt.__name__

        try:
            bn_func = getattr(bn, bn_name)
        except (AttributeError, NameError):  # pragma: no cover
            bn_func = None

        @functools.wraps(alt)
        def f(values, axis=None, skipna=True, **kwds):
            if len(self.kwargs) > 0:
                for k, v in compat.iteritems(self.kwargs):
                    if k not in kwds:
                        kwds[k] = v
            try:
                if values.size == 0:

                    # we either return np.nan or pd.NaT
                    if is_numeric_dtype(values):
                        values = values.astype('float64')
                    fill_value = na_value_for_dtype(values.dtype)

                    if values.ndim == 1:
                        return fill_value
                    else:
                        result_shape = (values.shape[:axis] +
                                        values.shape[axis + 1:])
                        result = np.empty(result_shape, dtype=values.dtype)
                        result.fill(fill_value)
                        return result

                if (_USE_BOTTLENECK and skipna and
                        _bn_ok_dtype(values.dtype, bn_name)):
                    result = bn_func(values, axis=axis, **kwds)

                    # prefer to treat inf/-inf as NA, but must compute the func
                    # twice :(
                    if _has_infs(result):
                        result = alt(values, axis=axis, skipna=skipna, **kwds)
                else:
                    result = alt(values, axis=axis, skipna=skipna, **kwds)
            except Exception:
                try:
                    result = alt(values, axis=axis, skipna=skipna, **kwds)
                except ValueError as e:
                    # we want to transform an object array
                    # ValueError message to the more typical TypeError
                    # e.g. this is normally a disallowed function on
                    # object arrays that contain strings

                    if is_object_dtype(values):
                        raise TypeError(e)
                    raise

            return result

        return f
