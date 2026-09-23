def wrap_logical_op_with_cast_to(to_type):
    def decorator(fn):
        def wrap_with_cast(g, input, other):
            return g.op("Cast", fn(g, input, other), to_i=sym_help.cast_pytorch_to_onnx[to_type])
        return wrap_with_cast
    return decorator
