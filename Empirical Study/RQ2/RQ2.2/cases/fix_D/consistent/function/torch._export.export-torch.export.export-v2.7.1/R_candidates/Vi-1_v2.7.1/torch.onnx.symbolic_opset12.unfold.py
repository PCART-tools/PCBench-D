@_onnx_symbolic("aten::unfold")
@symbolic_helper.parse_args("v", "i", "v", "v")
def unfold(g: jit_utils.GraphContext, input, dimension, size, step):
    const_size = symbolic_helper._maybe_get_const(size, "i")
    const_step = symbolic_helper._maybe_get_const(step, "i")
    if not symbolic_helper._is_value(const_size) and not symbolic_helper._is_value(
        const_step
    ):
        return opset9.unfold(g, input, dimension, const_size, const_step)

    sizedim = symbolic_helper._get_tensor_dim_size(input, dimension)
    if sizedim is not None:
        low_start = g.op("Constant", value_t=torch.tensor(0))
        low_end = g.op("Constant", value_t=torch.tensor(sizedim))
        hi_end = g.op("Constant", value_t=torch.tensor(sizedim + 1))
        low_indices = g.op("Range", low_start, low_end, step)
        hi_indices = g.op("Range", size, hi_end, step)

        low_size = symbolic_helper._size_helper(
            g, low_indices, g.op("Constant", value_t=torch.tensor(0))
        )
        hi_size = symbolic_helper._size_helper(
            g, hi_indices, g.op("Constant", value_t=torch.tensor(0))
        )

        ndim = symbolic_helper._get_tensor_rank(input)
        assert ndim is not None
        perm = list(range(0, ndim))
        perm.append(perm.pop(dimension))

        unsqueeze_list = []
        loop_condition = g.op("Constant", value_t=torch.tensor(1))
        loop_condition = g.op(
            "Cast", loop_condition, to_i=_C_onnx.TensorProtoDataType.BOOL
        )
        loop_len = g.op("Min", low_size, hi_size)

        loop, (loop_context,), _ = jit_utils.add_op_with_blocks(
            g, "Loop", loop_len, loop_condition, n_blocks=1
        )

        loop_block = loop_context.block
        block_input_iter = utils._add_input_to_block(loop_block)
        cond = utils._add_input_to_block(loop_block)  # noqa: F841

        starts = loop_context.op("Gather", low_indices, block_input_iter)
        ends = loop_context.op("Gather", hi_indices, block_input_iter)
        axes = loop_context.op("Constant", value_t=torch.tensor([2]))
        starts = symbolic_helper._unsqueeze_helper(loop_context, starts, [0])
        ends = symbolic_helper._unsqueeze_helper(loop_context, ends, [0])
        stack = loop_context.op("Slice", input, starts, ends, axes)

        unsqueeze = symbolic_helper._unsqueeze_helper(
            loop_context, loop_context.op("Transpose", stack, perm_i=perm), [dimension]
        )
        unsqueeze_list.append(unsqueeze)
        concat = loop_context.op("Concat", *unsqueeze_list, axis_i=0)

        cond_out = loop_context.op(
            "Cast", loop_condition, _C_onnx.TensorProtoDataType.BOOL
        )
        utils._add_output_to_block(loop_block, cond_out)
        utils._add_output_to_block(loop_block, concat)

        loop_output = loop.node().output()
        perm = [0, 1, 2, 3, 4]
        perm[0], perm[dimension + 1] = perm[dimension + 1], perm[0]
        transpose = g.op("Transpose", loop_output, perm_i=perm)
        squeeze = symbolic_helper._squeeze_helper(g, transpose, [0])

        return squeeze

    return symbolic_helper._unimplemented("Unfold", "input size not accessible")
