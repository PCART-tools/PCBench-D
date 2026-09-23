@_onnx_symbolic("aten::hardtanh")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "f", "f")
def hardtanh(g: jit_utils.GraphContext, self: _C.Value, min_val: float, max_val: float):
    return symbolic_helper._op_with_optional_float_cast(
        g, "Clip", self, min_f=min_val, max_f=max_val, opset_before=12
    )
