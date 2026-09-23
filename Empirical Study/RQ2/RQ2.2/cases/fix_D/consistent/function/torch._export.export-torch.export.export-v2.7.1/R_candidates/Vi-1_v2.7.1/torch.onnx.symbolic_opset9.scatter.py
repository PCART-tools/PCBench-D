@_onnx_symbolic("aten::scatter")
@symbolic_helper.parse_args("v", "i", "v", "v")
def scatter(g: jit_utils.GraphContext, self, dim, index, src):
    src_type = _type_utils.JitScalarType.from_value(
        src, _type_utils.JitScalarType.UNDEFINED
    )
    src = symbolic_helper._maybe_get_scalar(src)
    if symbolic_helper._is_value(src):
        return g.op("Scatter", self, index, src, axis_i=dim)
    else:
        # Check if scalar "src" has same type as self (PyTorch allows different
        # type for scalar src (but not when src is tensor)). If not, insert Cast node.
        self_scalar_type = _type_utils.JitScalarType.from_value(self)
        if self_scalar_type != src_type:
            src = g.op("Cast", src, to_i=self_scalar_type.onnx_type())
        return g.op("Scatter", self, index, expand_as(g, src, index), axis_i=dim)
