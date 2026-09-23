def register_inplace(aten_op, outplace_op):
    @register_decomposition(aten_op)
    def inplace_op(*args, **kwargs):
        out = outplace_op(*args, **kwargs)
        return args[0].copy_(out)

    return inplace_op
