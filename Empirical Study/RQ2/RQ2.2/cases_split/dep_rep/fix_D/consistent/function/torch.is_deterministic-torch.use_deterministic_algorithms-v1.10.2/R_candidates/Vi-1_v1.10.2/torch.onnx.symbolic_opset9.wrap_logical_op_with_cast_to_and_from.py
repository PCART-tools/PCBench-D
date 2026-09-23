def wrap_logical_op_with_cast_to_and_from(to_type):
    def decorator(fn):
        def wrap_with_cast(g, input, other):
            to_cast_func = globals()["_cast_{}".format(to_type)]
            from_cast_func = wrap_logical_op_with_cast_to(input.type().scalarType())(fn)
            return from_cast_func(g, to_cast_func(g, input, False), to_cast_func(g, other, False))
        return wrap_with_cast
    return decorator
