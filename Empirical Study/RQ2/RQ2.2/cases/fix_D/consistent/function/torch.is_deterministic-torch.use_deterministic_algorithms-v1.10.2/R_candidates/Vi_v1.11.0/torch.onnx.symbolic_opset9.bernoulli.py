def bernoulli(g, input, generator=None, out=None):
    if out is not None:
        _unimplemented("Bernoulli", "out parameter is not supported for bernoulli")
    if generator is not None and not sym_help._is_none(generator):
        _unimplemented("Bernoulli", "generator is not supported for bernoulli")

    dtype = sym_help._try_get_scalar_type(input)
    if dtype is None:
        return _unimplemented("Bernoulli", "input dtype not accessible")
    p = g.op("RandomUniformLike", input, high_f=1.0, low_f=0.0, dtype_i=sym_help.cast_pytorch_to_onnx[dtype])
    output = g.op("Less", p, input)
    return g.op("Cast", output, to_i=sym_help.cast_pytorch_to_onnx[dtype])
