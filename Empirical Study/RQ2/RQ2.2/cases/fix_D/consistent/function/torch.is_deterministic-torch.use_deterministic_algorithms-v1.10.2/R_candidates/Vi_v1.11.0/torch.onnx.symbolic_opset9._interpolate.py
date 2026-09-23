def _interpolate(name, dim, interpolate_mode):
    def symbolic_fn(g, input, output_size, *args):
        scales, align_corners = sym_help._get_interpolate_attributes(g, interpolate_mode, args)
        sym_help._interpolate_warning(interpolate_mode)
        align_corners = sym_help._maybe_get_scalar(align_corners)
        if align_corners:
            return _unimplemented(name, "align_corners == True")
        if scales is None:
            scales = sym_help._interpolate_size_to_scales(g, input, output_size, dim)
        return g.op("Upsample", input, scales, mode_s=interpolate_mode)
    return symbolic_fn
