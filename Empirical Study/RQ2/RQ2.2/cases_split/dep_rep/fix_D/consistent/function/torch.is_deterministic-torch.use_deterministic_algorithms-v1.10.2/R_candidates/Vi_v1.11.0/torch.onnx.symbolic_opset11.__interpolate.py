def __interpolate(g, input, size, scale_factor, mode, align_corners, recompute_scale_factor, antialias):
    return sym_help.__interpolate_helper(g, input, size, scale_factor, mode, align_corners, recompute_scale_factor)
