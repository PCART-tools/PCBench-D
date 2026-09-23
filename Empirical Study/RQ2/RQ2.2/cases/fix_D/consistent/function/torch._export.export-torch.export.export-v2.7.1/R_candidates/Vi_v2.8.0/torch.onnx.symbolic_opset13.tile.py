@_onnx_symbolic("aten::tile")
def tile(g: jit_utils.GraphContext, self, dims):
    self_shape = g.op("Shape", self)
    self_rank = g.op("Size", self_shape)
    dims_rank = g.op("Size", dims)
    diff = g.op("Sub", self_rank, dims_rank)
    const_zero = g.op("Constant", value_t=torch.tensor([0]))

    # 1. If dims is shorter than self.shape pad dims with 1
    dims_shorter_than_self_shape = g.op("Greater", diff, const_zero)
    (
        if_op_greater,
        (if_context_greater, else_context_greater),
        _,
    ) = jit_utils.add_op_with_blocks(
        g, "If", dims_shorter_than_self_shape, n_blocks=2, outputs=1
    )
    const_one = if_context_greater.op("Constant", value_t=torch.LongTensor([1]))
    diff_1d_greater = if_context_greater.op("Reshape", diff, const_one)
    exapnd_ones_greater = if_context_greater.op("Expand", const_one, diff_1d_greater)
    dims_ = if_context_greater.op("Concat", exapnd_ones_greater, dims, axis_i=0)
    utils._add_output_to_block(if_context_greater.block, dims_)
    identity_dim = else_context_greater.op("Identity", dims)
    utils._add_output_to_block(else_context_greater.block, identity_dim)
    dims_final = if_op_greater.node().output()

    # 2. If dims is longer than self.shape pad self.shape with 1
    dims_longer_than_self_shape = g.op("Less", diff, const_zero)
    (
        if_op_less,
        (if_context_less, else_context_less),
        _,
    ) = jit_utils.add_op_with_blocks(
        g, "If", dims_longer_than_self_shape, n_blocks=2, outputs=1
    )
    const_one = if_context_less.op("Constant", value_t=torch.LongTensor([1]))
    diff_1d_less = if_context_less.op(
        "Reshape",
        if_context_less.op("Abs", diff),
        const_one,
    )
    exapnd_ones_less = if_context_less.op("Expand", const_one, diff_1d_less)
    self_final_shape = if_context_less.op(
        "Concat", exapnd_ones_less, self_shape, axis_i=0
    )
    self_ = if_context_less.op("Reshape", self, self_final_shape)
    utils._add_output_to_block(if_context_less.block, self_)
    identity_self = else_context_less.op("Identity", self)
    utils._add_output_to_block(else_context_less.block, identity_self)
    self_final = if_op_less.node().output()

    dims_final = g.op("Cast", dims_final, to_i=_C_onnx.TensorProtoDataType.INT64)
    return g.op("Tile", self_final, dims_final)
