@_onnx_symbolic("aten::pixel_shuffle")
@symbolic_helper.parse_args("v", "i")
def pixel_shuffle(g: jit_utils.GraphContext, self, upscale_factor):
    rank = symbolic_helper._get_tensor_rank(self)
    if rank is not None and rank != 4:
        return symbolic_helper._unimplemented("pixel_shuffle", "only support 4d input")
    return g.op("DepthToSpace", self, blocksize_i=upscale_factor, mode_s="CRD")
