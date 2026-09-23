def __interpolate(g, input, size, scale_factor, mode , align_corners, recompute_scale_factor, antialias):
    scales, mode = sym_help._interpolate_get_scales_and_mode(g, input, size, scale_factor,
                                                             mode , align_corners)
    return g.op("Resize", input, scales, mode_s=mode)
