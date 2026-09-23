@_onnx_symbolic("aten::clamp_min")
@symbolic_helper.parse_args("v", "v")
def clamp_min(g: jit_utils.GraphContext, self, min):
    min = g.op("Cast", min, to_i=_type_utils.JitScalarType.from_value(self).onnx_type())
    if symbolic_helper._get_tensor_rank(min) == 0:
        max = opset9.unused(g)
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, min, max, opset_before=12
        )
    else:
        return symbolic_helper._op_with_optional_float_cast(
            g, "Max", self, min, opset_before=12
        )
