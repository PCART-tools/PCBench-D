@parse_args("v", "t", "is", "i")
def norm(g, self, p, dim, keepdim):
    if p == 1:
        f = _reduce_op_symbolic("ReduceL1")
    elif p == 2:
        f = _reduce_op_symbolic("ReduceL2")
    else:
        raise RuntimeError("ONNX export only p-norms with p of 1 or 2")
    return f(g, self, dim=dim, keepdim=keepdim)
