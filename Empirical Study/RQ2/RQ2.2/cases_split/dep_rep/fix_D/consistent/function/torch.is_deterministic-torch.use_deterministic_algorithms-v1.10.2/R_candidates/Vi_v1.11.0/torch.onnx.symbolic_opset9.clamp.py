def clamp(g, self, min, max):
    # min or max may be None that we need to dispatch to
    # Clip separately, as ONNX does not have None syntax
    if sym_help._is_none(min):
        return clamp_max(g, self, max)
    elif sym_help._is_none(max):
        return clamp_min(g, self, min)
    else:
        if sym_help._is_constant(min) and sym_help._is_constant(max):
            return g.op("Clip", self, min_f=_parse_arg(min, "f"), max_f=_parse_arg(max, "f"))
        else:
            return clamp_max(g, clamp_min(g, self, min), max)
