def _interpolate(name, dim, interpolate_mode):
    def symbolic_fn(g, input, output_size, *args):
        scales, align_corners = sym_help._get_interpolate_attributes(g, interpolate_mode, args)
        sym_help._interpolate_warning(interpolate_mode)
        align_corners = sym_help._maybe_get_scalar(align_corners)
        if align_corners:
            return _unimplemented(name, "align_corners == True")
        output_size = sym_help._maybe_get_const(output_size, "is")
        if sym_help._is_value(output_size):
            return _unimplemented(name, "torch._C.Value (output_size) indexing")
        if scales is None:
            scales = [1. if i < 2 else
                      float(output_size[-(dim - i)]) / float(input.type().sizes()[-(dim - i)])
                      for i in range(0, dim)]
        return g.op("Upsample", input, mode_s=interpolate_mode, scales_f=scales)
    return symbolic_fn
