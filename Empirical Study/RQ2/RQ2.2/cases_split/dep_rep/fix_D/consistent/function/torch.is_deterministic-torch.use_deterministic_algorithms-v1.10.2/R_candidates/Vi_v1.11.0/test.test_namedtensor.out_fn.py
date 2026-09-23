def out_fn(operator):
    @functools.wraps(operator)
    def fn(*inputs):
        return operator(*inputs[1:], out=inputs[0])
    return fn
