@parse_args("v", "t", "t", "t")
def elu(g, input, alpha, scale, input_scale):
    if scale and scale != 1.:
        return _unimplemented("scale", "does not support scale in Elu")
    if input_scale and input_scale != 1.:
        return _unimplemented("input_scale", "does not support input_scale in Elu")
    # See Note [Export inplace]
    return g.op("Elu", input, alpha_f=sym_help._scalar(alpha))
