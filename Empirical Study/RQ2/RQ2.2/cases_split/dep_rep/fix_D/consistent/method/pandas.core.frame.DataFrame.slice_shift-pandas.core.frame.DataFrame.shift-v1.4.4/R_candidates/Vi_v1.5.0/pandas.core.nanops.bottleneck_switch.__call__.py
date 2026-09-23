    def __call__(self, alt: F) -> F:
        bn_name = self.name or alt.__name__

        try:
            bn_func = getattr(bn, bn_name)
        except (AttributeError, NameError):  # pragma: no cover
            bn_func = None

        @functools.wraps(alt)
        def f(
            values: np.ndarray,
            *,
            axis: int | None = None,
            skipna: bool = True,
            **kwds,
        ):
            if len(self.kwargs) > 0:
                for k, v in self.kwargs.items():
                    if k not in kwds:
                        kwds[k] = v

            if values.size == 0 and kwds.get("min_count") is None:
                # We are empty, returning NA for our type
                # Only applies for the default `min_count` of None
                # since that affects how empty arrays are handled.
                # TODO(GH-18976) update all the nanops methods to
                # correctly handle empty inputs and remove this check.
                # It *may* just be `var`
                return _na_for_min_count(values, axis)

            if _USE_BOTTLENECK and skipna and _bn_ok_dtype(values.dtype, bn_name):
                if kwds.get("mask", None) is None:
                    # `mask` is not recognised by bottleneck, would raise
                    #  TypeError if called
                    kwds.pop("mask", None)
                    result = bn_func(values, axis=axis, **kwds)

                    # prefer to treat inf/-inf as NA, but must compute the func
                    # twice :(
                    if _has_infs(result):
                        result = alt(values, axis=axis, skipna=skipna, **kwds)
                else:
                    result = alt(values, axis=axis, skipna=skipna, **kwds)
            else:
                result = alt(values, axis=axis, skipna=skipna, **kwds)

            return result

        return cast(F, f)
