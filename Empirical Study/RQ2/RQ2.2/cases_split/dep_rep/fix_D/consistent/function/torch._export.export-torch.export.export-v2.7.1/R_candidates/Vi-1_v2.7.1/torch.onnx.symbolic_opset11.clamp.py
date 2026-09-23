@_onnx_symbolic("aten::clamp")
def clamp(g: jit_utils.GraphContext, self, min, max):
    def _cast_if_not_none(tensor, dtype):
        if tensor is not None and not symbolic_helper._is_none(tensor):
            return g.op(
                "Cast",
                tensor,
                to_i=dtype.onnx_type(),
            )
        else:
            return tensor

    scalar_type = _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.UNDEFINED
    )
    if scalar_type != _type_utils.JitScalarType.UNDEFINED:
        min = _cast_if_not_none(min, scalar_type)
        max = _cast_if_not_none(max, scalar_type)

    if symbolic_helper._is_none(min):
        return clamp_max(g, self, max)
    elif symbolic_helper._is_none(max):
        return clamp_min(g, self, min)
    else:
        if (
            symbolic_helper._get_tensor_rank(min) == 0
            and symbolic_helper._get_tensor_rank(max) == 0
        ):
            return symbolic_helper._op_with_optional_float_cast(
                g, "Clip", self, min, max, opset_before=12
            )
        else:
            return clamp_max(g, clamp_min(g, self, min), max)
