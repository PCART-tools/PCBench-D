    def __array_ufunc__(self, ufunc: np.ufunc, method: str, *inputs, **kwargs):
        # for binary ops, use our custom dunder methods
        result = arraylike.maybe_dispatch_ufunc_to_dunder_op(
            self, ufunc, method, *inputs, **kwargs
        )
        if result is not NotImplemented:
            return result

        if "out" in kwargs:
            # e.g. test_numpy_ufuncs_out
            return arraylike.dispatch_ufunc_with_out(
                self, ufunc, method, *inputs, **kwargs
            )

        if method == "reduce":
            # e.g. TestCategoricalAnalytics::test_min_max_ordered
            result = arraylike.dispatch_reduction_ufunc(
                self, ufunc, method, *inputs, **kwargs
            )
            if result is not NotImplemented:
                return result

        # for all other cases, raise for now (similarly as what happens in
        # Series.__array_prepare__)
        raise TypeError(
            f"Object with dtype {self.dtype} cannot perform "
            f"the numpy op {ufunc.__name__}"
        )
