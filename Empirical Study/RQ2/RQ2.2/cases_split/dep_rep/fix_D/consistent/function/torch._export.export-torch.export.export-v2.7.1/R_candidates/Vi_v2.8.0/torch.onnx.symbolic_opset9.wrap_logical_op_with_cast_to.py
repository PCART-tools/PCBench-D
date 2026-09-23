def wrap_logical_op_with_cast_to(to_type):
    def decorator(fn):
        @functools.wraps(fn)
        def wrap_with_cast(g, input, other):
            to_cast_func = globals()[f"_cast_{to_type}"]
            return fn(g, to_cast_func(g, input, False), to_cast_func(g, other, False))

        return wrap_with_cast

    return decorator
