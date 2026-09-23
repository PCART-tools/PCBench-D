@_onnx_symbolic("aten::clamp_max")
@symbolic_helper.parse_args("v", "v")
def clamp_max(g: jit_utils.GraphContext, self, max):
    if symbolic_helper._is_constant(max):
        return symbolic_helper._op_with_optional_float_cast(
            g, "Clip", self, max_f=symbolic_helper._parse_arg(max, "f"), opset_before=12
        )
    else:
        dtype = _type_utils.JitScalarType.from_value(self)
        max = g.op("Cast", max, to_i=dtype.onnx_type())
        return symbolic_helper._op_with_optional_float_cast(
            g, "Min", self, max, opset_before=12
        )
