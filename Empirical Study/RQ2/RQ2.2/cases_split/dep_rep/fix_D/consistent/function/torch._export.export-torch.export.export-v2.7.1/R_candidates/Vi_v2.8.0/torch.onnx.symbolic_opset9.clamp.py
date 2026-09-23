@_onnx_symbolic("aten::clamp")
def clamp(g: jit_utils.GraphContext, self, min, max):
    # min or max may be None that we need to dispatch to
    # Clip separately, as ONNX does not have None syntax
    if symbolic_helper._is_none(min):
        return clamp_max(g, self, max)
    elif symbolic_helper._is_none(max):
        return clamp_min(g, self, min)
    else:
        if symbolic_helper._is_constant(min) and symbolic_helper._is_constant(max):
            return symbolic_helper._op_with_optional_float_cast(
                g,
                "Clip",
                self,
                min_f=symbolic_helper._parse_arg(min, "f"),
                max_f=symbolic_helper._parse_arg(max, "f"),
                opset_before=12,
            )
        else:
            return clamp_max(g, clamp_min(g, self, min), max)
