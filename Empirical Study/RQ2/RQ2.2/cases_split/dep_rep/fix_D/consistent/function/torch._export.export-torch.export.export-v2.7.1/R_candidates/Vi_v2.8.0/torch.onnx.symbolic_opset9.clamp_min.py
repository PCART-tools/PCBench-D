@_onnx_symbolic("aten::clamp_min")
@symbolic_helper.parse_args("v", "v")
def clamp_min(g: jit_utils.GraphContext, self, min):
    if symbolic_helper._is_constant(min):
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, min_f=symbolic_helper._parse_arg(min, "f"), opset_before=12
        )
    else:
        dtype = _type_utils.JitScalarType.from_value(self)
        min = g.op("Cast", min, to_i=dtype.onnx_type())
        return symbolic_helper._op_with_optional_float_cast(
            g, "Max", self, min, opset_before=12
        )
