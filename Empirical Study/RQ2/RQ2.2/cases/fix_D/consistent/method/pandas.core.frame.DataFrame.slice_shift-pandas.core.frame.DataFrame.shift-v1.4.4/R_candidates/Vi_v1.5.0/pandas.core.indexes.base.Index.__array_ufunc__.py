    def __array_ufunc__(self, ufunc: np.ufunc, method: str_t, *inputs, **kwargs):
        if any(isinstance(other, (ABCSeries, ABCDataFrame)) for other in inputs):
            return NotImplemented

        # TODO(2.0) the 'and', 'or' and 'xor' dunder methods are currently set
        # operations and not logical operations, so don't dispatch
        # This is deprecated, so this full 'if' clause can be removed once
        # deprecation is enforced in 2.0
        if not (
            method == "__call__"
            and ufunc in (np.bitwise_and, np.bitwise_or, np.bitwise_xor)
        ):
            result = arraylike.maybe_dispatch_ufunc_to_dunder_op(
                self, ufunc, method, *inputs, **kwargs
            )
            if result is not NotImplemented:
                return result

        if "out" in kwargs:
            # e.g. test_dti_isub_tdi
            return arraylike.dispatch_ufunc_with_out(
                self, ufunc, method, *inputs, **kwargs
            )

        if method == "reduce":
            result = arraylike.dispatch_reduction_ufunc(
                self, ufunc, method, *inputs, **kwargs
            )
            if result is not NotImplemented:
                return result

        new_inputs = [x if x is not self else x._values for x in inputs]
        result = getattr(ufunc, method)(*new_inputs, **kwargs)
        if ufunc.nout == 2:
            # i.e. np.divmod, np.modf, np.frexp
            return tuple(self.__array_wrap__(x) for x in result)

        return self.__array_wrap__(result)
