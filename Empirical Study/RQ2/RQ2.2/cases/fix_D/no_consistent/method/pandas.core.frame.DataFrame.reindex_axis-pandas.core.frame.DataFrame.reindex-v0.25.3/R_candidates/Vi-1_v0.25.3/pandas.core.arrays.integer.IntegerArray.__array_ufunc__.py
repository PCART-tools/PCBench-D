    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # For IntegerArray inputs, we apply the ufunc to ._data
        # and mask the result.
        if method == "reduce":
            # Not clear how to handle missing values in reductions. Raise.
            raise NotImplementedError("The 'reduce' method is not supported.")
        out = kwargs.get("out", ())

        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (IntegerArray,)):
                return NotImplemented

        # for binary ops, use our custom dunder methods
        result = ops.maybe_dispatch_ufunc_to_dunder_op(
            self, ufunc, method, *inputs, **kwargs
        )
        if result is not NotImplemented:
            return result

        mask = np.zeros(len(self), dtype=bool)
        inputs2 = []
        for x in inputs:
            if isinstance(x, IntegerArray):
                mask |= x._mask
                inputs2.append(x._data)
            else:
                inputs2.append(x)

        def reconstruct(x):
            # we don't worry about scalar `x` here, since we
            # raise for reduce up above.

            if is_integer_dtype(x.dtype):
                m = mask.copy()
                return IntegerArray(x, m)
            else:
                x[mask] = np.nan
            return x

        result = getattr(ufunc, method)(*inputs2, **kwargs)
        if isinstance(result, tuple):
            tuple(reconstruct(x) for x in result)
        else:
            return reconstruct(result)
