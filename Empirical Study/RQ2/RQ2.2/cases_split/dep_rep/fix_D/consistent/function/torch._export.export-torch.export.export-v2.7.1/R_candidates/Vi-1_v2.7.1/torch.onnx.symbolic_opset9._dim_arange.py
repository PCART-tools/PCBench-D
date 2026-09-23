@_onnx_symbolic("aten::_dim_arange")
@symbolic_helper.parse_args("v", "i")
def _dim_arange(g: jit_utils.GraphContext, like, dim):
    like_shape = g.op("Shape", like)
    stop = g.op(
        "Gather", like_shape, g.op("Constant", value_t=torch.tensor(dim)), axis_i=0
    )
    # aten::arange(Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
    return arange(g, stop, 4, None, None, None)
