    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # for binary ops, use our custom dunder methods
        result = ops.maybe_dispatch_ufunc_to_dunder_op(
            self, ufunc, method, *inputs, **kwargs
        )
        if result is not NotImplemented:
            return result

        # for all other cases, raise for now (similarly as what happens in
        # Series.__array_prepare__)
        raise TypeError(
            "Object with dtype {dtype} cannot perform "
            "the numpy op {op}".format(dtype=self.dtype, op=ufunc.__name__)
        )
