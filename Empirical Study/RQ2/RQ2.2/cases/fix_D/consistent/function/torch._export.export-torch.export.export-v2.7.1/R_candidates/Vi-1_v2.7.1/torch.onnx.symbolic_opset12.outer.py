@_onnx_symbolic("aten::outer")
@symbolic_helper.parse_args("v", "v")
def outer(g: jit_utils.GraphContext, input, other):
    # make sure to cast other to self's type
    if _type_utils.JitScalarType.from_value(
        other, _type_utils.JitScalarType.UNDEFINED
    ) != _type_utils.JitScalarType.from_value(input):
        other = g.op(
            "Cast",
            other,
            to_i=_type_utils.JitScalarType.from_value(input).onnx_type(),
        )
    return _einsum_helper(g, "i,j->ij", [input, other])
