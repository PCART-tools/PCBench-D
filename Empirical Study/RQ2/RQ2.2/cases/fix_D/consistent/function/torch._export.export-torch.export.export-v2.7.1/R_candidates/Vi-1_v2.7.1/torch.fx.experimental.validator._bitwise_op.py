    def _bitwise_op(bitwise_func, bool_func):
        @functools.wraps(bitwise_func)
        def wrapper(self, *args):
            if bool_func is not None and all(
                isinstance(arg, z3.BoolRef) for arg in args
            ):
                return bool_func(*args)

            wrapped_args = tuple(z3.Int2BV(a, 64) for a in args)
            return z3.BV2Int(bitwise_func(*wrapped_args))

        return wrapper
