def __interpolate(g, input, size, scale_factor, mode, align_corners, recompute_scale_factor):
    align_corners = sym_help._maybe_get_const(align_corners, "b")
    if not sym_help._is_none(align_corners) and align_corners:
        return _unimplemented("interpolate", "align_corners == True")

    if not sym_help._is_none(scale_factor) and sym_help._is_value(scale_factor):
        return _unimplemented("interpolate", "dynamic scales in opset 8")

    if not sym_help._is_none(size) and sym_help._is_value(size):
        return _unimplemented("interpolate", "dynamic size in opset 8")

    scales, mode = sym_help._interpolate_get_scales_and_mode(g, input, size, scale_factor,
                                                             mode , align_corners)
    return g.op("Upsample", input, mode_s=mode, scales_f=scales)
