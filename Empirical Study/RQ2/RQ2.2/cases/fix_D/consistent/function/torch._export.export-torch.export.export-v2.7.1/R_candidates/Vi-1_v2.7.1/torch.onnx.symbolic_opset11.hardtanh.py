@_onnx_symbolic("aten::hardtanh")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "f", "f")
def hardtanh(g: jit_utils.GraphContext, self: _C.Value, min_val: float, max_val: float):
    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.FLOAT
    )
    min_val = g.op(
        "Constant",
        value_t=torch.tensor(min_val, dtype=scalar_type.dtype()),
    )
    max_val = g.op(
        "Constant",
        value_t=torch.tensor(max_val, dtype=scalar_type.dtype()),
    )
    return symbolic_helper._op_with_optional_float_cast(
        g, "Clip", self, min_val, max_val, opset_before=12
    )
