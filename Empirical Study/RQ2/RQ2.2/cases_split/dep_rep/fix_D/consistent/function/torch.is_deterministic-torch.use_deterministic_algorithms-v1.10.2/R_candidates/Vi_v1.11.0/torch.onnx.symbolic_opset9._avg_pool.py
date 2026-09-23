def _avg_pool(name, tuple_fn):
    @parse_args("v", "is", "is", "is", "i", "i", "none")
    def symbolic_fn(g, input, kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override=None):
        if not stride:
            stride = kernel_size
        padding = sym_help._avgpool_helper(tuple_fn, padding, kernel_size, stride, divisor_override, name)
        if ceil_mode:
            padding_ceil = get_pool_ceil_padding(input, kernel_size, stride, padding)
        if count_include_pad:
            input = g.op("Pad", input,
                         pads_i=((0,) * 2 + padding) * 2,
                         mode_s="constant",
                         value_f=0.)
            padding = (0,) * len(padding)
        if ceil_mode:
            padding = padding + tuple(a + b for (a, b) in zip(padding_ceil, padding))
        else:
            padding = padding * 2
        output = g.op("AveragePool", input,
                      kernel_shape_i=tuple_fn(kernel_size),
                      strides_i=tuple_fn(stride),
                      pads_i=padding)
        return output
    return symbolic_fn
