def _trunc_divide(g, self, other):
    out = g.op("Div", self, other)
    # the correct operation is truncate, which is not supported in ONNX,
    # we cannot call floor since it will behave differently for negative numbers
    # (eg. -0.1 should become -0 )
    # - if scalar_type information are not available, assume that
    # we need to call floor (treat as float)
    out = g.op("Cast", out, to_i=sym_help.cast_pytorch_to_onnx["Long"])

    # Matching PyTorch's behavior:
    # - if self is fp the output's type is self's type
    # - if self is not fp and other is fp, the output is of type "Float"
    # - self is not fp and other is not fp, the output's type is self's output type
    # - the output type defaults to Float
    scalar_type = self.type().scalarType()

    if scalar_type is not None:
        if not sym_help._is_fp(self) and \
           other.type().scalarType() is not None and \
           sym_help._is_fp(other):
            out = g.op("Cast", out, to_i=sym_help.cast_pytorch_to_onnx["Float"])
        else:
            out = g.op("Cast", out, to_i=sym_help.cast_pytorch_to_onnx[scalar_type])
    else:
        out = g.op("Cast", out, to_i=sym_help.cast_pytorch_to_onnx["Float"])
    return out
