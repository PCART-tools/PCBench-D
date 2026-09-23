@_onnx_symbolic("aten::pixel_shuffle")
@symbolic_helper.parse_args("v", "i")
def pixel_shuffle(g: jit_utils.GraphContext, self, upscale_factor):
    dims = symbolic_helper._get_tensor_sizes(self)
    if len(dims) != 4:
        return symbolic_helper._unimplemented(
            "pixel_shuffle", "only support 4d input", self
        )
    if any(i is None for i in dims[1:]):
        after_view = symbolic_helper._reshape_helper(
            g,
            symbolic_helper._unsqueeze_helper(g, self, [2, 3]),
            g.op(
                "Constant",
                value_t=torch.tensor([0, -1, upscale_factor, upscale_factor, 0, 0]),
            ),
            allowzero=0,
        )
        after_transpose = g.op("Transpose", after_view, perm_i=[0, 1, 4, 2, 5, 3])
        # For dynamic input shapes, two reshapes are performed
        reshape_h = symbolic_helper._reshape_helper(
            g,
            after_transpose,
            g.op("Constant", value_t=torch.tensor([0, 0, -1, 1, 0, 0])),
            allowzero=0,
        )
        reshape_w = symbolic_helper._reshape_helper(
            g,
            reshape_h,
            g.op("Constant", value_t=torch.tensor([0, 0, 0, 0, -1, 1])),
            allowzero=0,
        )
        return symbolic_helper._squeeze_helper(g, reshape_w, [3, 5])
    else:
        output_channel = dims[1] // upscale_factor // upscale_factor
        after_view = symbolic_helper._reshape_helper(
            g,
            self,
            g.op(
                "Constant",
                value_t=torch.tensor(
                    [
                        -1,
                        output_channel,
                        upscale_factor,
                        upscale_factor,
                        dims[2],
                        dims[3],
                    ]
                ),
            ),
            allowzero=0,
        )
        after_transpose = g.op("Transpose", after_view, perm_i=[0, 1, 4, 2, 5, 3])
        return symbolic_helper._reshape_helper(
            g,
            after_transpose,
            g.op(
                "Constant",
                value_t=torch.tensor(
                    [
                        -1,
                        output_channel,
                        dims[2] * upscale_factor,
                        dims[3] * upscale_factor,
                    ]
                ),
            ),
            allowzero=0,
        )
