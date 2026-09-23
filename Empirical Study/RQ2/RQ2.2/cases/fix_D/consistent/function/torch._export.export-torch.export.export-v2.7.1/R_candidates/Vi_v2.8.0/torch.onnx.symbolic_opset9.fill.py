@_onnx_symbolic("aten::fill")
@symbolic_helper.parse_args("v", "v")
def fill(g: jit_utils.GraphContext, self, value):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    return full_like(g, self, value, scalar_type)
