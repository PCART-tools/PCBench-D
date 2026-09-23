@_onnx_symbolic("aten::hstack")
def hstack(g: jit_utils.GraphContext, tensor_list: _C.Value):
    tensor_list = atleast_1d(g, tensor_list)
    first_tensor = g.op(
        "SequenceAt",
        tensor_list,
        g.op("Constant", value_t=torch.tensor(0, dtype=torch.long)),
    )
    first_tensor_shape = g.op("Shape", first_tensor)
    first_tensor_dim = g.op("Size", first_tensor_shape)

    const_one = g.op("Constant", value_t=torch.tensor(1, dtype=torch.long))
    equal_to_one = g.op("Equal", first_tensor_dim, const_one)

    (
        if_op_greater,
        (if_context_equal, else_context_equal),
        _,
    ) = jit_utils.add_op_with_blocks(g, "If", equal_to_one, n_blocks=2, outputs=1)
    result_if = if_context_equal.op(
        "ConcatFromSequence", tensor_list, axis_i=0, new_axis_i=0
    )
    utils._add_output_to_block(if_context_equal.block, result_if)
    result_else = else_context_equal.op(
        "ConcatFromSequence", tensor_list, axis_i=1, new_axis_i=0
    )
    utils._add_output_to_block(else_context_equal.block, result_else)
    result = if_op_greater.node().output()

    return result
