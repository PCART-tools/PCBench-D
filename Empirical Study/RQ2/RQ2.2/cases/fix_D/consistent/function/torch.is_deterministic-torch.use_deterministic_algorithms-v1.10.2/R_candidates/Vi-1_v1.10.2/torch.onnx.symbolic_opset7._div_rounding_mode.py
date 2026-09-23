@parse_args("v", "v", "s")
def _div_rounding_mode(g, self, other, rounding_mode):
    if rounding_mode == "floor":
        return _floor_divide(g, self, other)
    else:
        return sym_opset9._div_rounding_mode(g, self, other, rounding_mode)
