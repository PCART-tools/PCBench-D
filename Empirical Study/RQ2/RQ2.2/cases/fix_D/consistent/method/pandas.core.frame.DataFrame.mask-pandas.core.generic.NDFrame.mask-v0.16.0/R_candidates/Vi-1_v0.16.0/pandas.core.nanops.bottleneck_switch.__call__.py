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
                if self.zero_value is not None and values.size == 0:
                    if values.ndim == 1:

                        # wrap the 0's if needed
                        if is_timedelta64_dtype(values):
                            return lib.Timedelta(0)
                        return 0
                    else:
                        result_shape = (values.shape[:axis] +
                                        values.shape[axis + 1:])
                        result = np.empty(result_shape)
                        result.fill(0)
                        return result

                if _USE_BOTTLENECK and skipna and _bn_ok_dtype(values.dtype,
                                                               bn_name):
                    result = bn_func(values, axis=axis, **kwds)

                    # prefer to treat inf/-inf as NA, but must compute the func
                    # twice :(
                    if _has_infs(result):
                        result = alt(values, axis=axis, skipna=skipna, **kwds)
                else:
                    result = alt(values, axis=axis, skipna=skipna, **kwds)
            except Exception:
                result = alt(values, axis=axis, skipna=skipna, **kwds)

            return result

        return f
