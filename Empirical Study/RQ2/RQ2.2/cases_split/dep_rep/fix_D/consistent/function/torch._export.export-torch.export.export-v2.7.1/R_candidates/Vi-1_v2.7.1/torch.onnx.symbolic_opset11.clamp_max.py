@_onnx_symbolic("aten::clamp_max")
@symbolic_helper.parse_args("v", "v")
def clamp_max(g: jit_utils.GraphContext, self, max):
    max = g.op("Cast", max, to_i=_type_utils.JitScalarType.from_value(self).onnx_type())
    if symbolic_helper._get_tensor_rank(max) == 0:
        min = opset9.unused(g)
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, min, max, opset_before=12
        )
    else:
        return symbolic_helper._op_with_optional_float_cast(
            g, "Min", self, max, opset_before=12
        )
