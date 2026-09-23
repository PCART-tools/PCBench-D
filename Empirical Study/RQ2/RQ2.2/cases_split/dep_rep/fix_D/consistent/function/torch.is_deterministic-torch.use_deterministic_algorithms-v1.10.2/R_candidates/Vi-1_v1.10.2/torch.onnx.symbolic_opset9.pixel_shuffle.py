@parse_args("v", "i")
def pixel_shuffle(g, self, upscale_factor):
    dims = sym_help._get_tensor_sizes(self)
    if len(dims) != 4:
        return _unimplemented("pixel_shuffle", "only support 4d input")
    if any([i is None for i in dims[1:]]):
        return _unimplemented("pixel_shuffle", "only support static input shape, except for batch size")
    output_channel = dims[1] // upscale_factor // upscale_factor
    after_view = sym_help._reshape_helper(g, self,
                                          g.op("Constant", value_t=torch.tensor([-1, output_channel,
                                                                                upscale_factor, upscale_factor,
                                                                                dims[2], dims[3]])),
                                          allowzero=0)
    after_transpose = g.op("Transpose", after_view, perm_i=[0, 1, 4, 2, 5, 3])
    return sym_help._reshape_helper(g, after_transpose,
                                    g.op("Constant", value_t=torch.tensor([-1, output_channel,
                                                                          dims[2] * upscale_factor,
                                                                          dims[3] * upscale_factor])),
                                    allowzero=0)
