@parse_args("v", "v", "s")
def _div_rounding_mode(g, self, other, rounding_mode):
    if rounding_mode is None:
        return true_divide(g, self, other)
    elif rounding_mode == "floor":
        return _floor_divide(g, self, other)
    elif rounding_mode == "trunc":
        return _trunc_divide(g, self, other)
    else:
        raise RuntimeError(f'Unsupported rounding mode: "{rounding_mode}". Expected None, "floor" or "trunc"')
