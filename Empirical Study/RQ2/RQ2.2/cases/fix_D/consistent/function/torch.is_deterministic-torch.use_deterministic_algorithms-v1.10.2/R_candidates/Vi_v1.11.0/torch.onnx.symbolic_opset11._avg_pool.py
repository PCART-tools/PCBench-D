def _avg_pool(name, tuple_fn):
    @parse_args("v", "is", "is", "is", "i", "i", "none")
    def symbolic_fn(g, input, kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override=None):
        padding = sym_help._avgpool_helper(tuple_fn, padding, kernel_size, stride, divisor_override, name)
        if not stride:
            stride = kernel_size
        if count_include_pad:
            input = g.op("Pad", input,
                         g.op("Constant", value_t=torch.tensor(((0,) * 2 + padding) * 2)), mode_s="constant")
            padding = (0,) * len(padding)
        output = g.op("AveragePool", input,
                      kernel_shape_i=tuple_fn(kernel_size),
                      strides_i=tuple_fn(stride),
                      pads_i=padding * 2,
                      ceil_mode_i=ceil_mode)
        return output
    return symbolic_fn
