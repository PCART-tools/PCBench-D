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
                if values.size == 0 and kwds.get('min_count') is None:
                    # We are empty, returning NA for our type
                    # Only applies for the default `min_count` of None
                    # since that affects how empty arrays are handled.
                    # TODO(GH-18976) update all the nanops methods to
                    # correctly handle empty inputs and remove this check.
                    # It *may* just be `var`
                    return _na_for_min_count(values, axis)

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
