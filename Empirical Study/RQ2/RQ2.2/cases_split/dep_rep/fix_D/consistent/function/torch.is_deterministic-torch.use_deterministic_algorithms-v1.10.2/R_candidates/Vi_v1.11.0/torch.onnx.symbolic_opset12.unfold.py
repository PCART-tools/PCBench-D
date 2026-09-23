@parse_args("v", "i", "v", "v")
def unfold(g, input, dimension, size, step):
    const_size = sym_help._maybe_get_const(size, "i")
    const_step = sym_help._maybe_get_const(step, "i")
    if not sym_help._is_value(const_size) and not sym_help._is_value(const_step):
        from torch.onnx.symbolic_opset9 import unfold as _unfold
        return _unfold(g, input, dimension, const_size, const_step)
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, operator_s="unfold", dimension_i=dimension, size_i=size, step_i=step)

    sizedim = sym_help._get_tensor_dim_size(input, dimension)
    if sizedim is not None:
        low_start = g.op("Constant", value_t=torch.tensor(0))
        low_end = g.op("Constant", value_t=torch.tensor(sizedim))
        hi_end = g.op("Constant", value_t=torch.tensor(sizedim + 1))
        low_indices = g.op("Range", low_start, low_end, step)
        hi_indices = g.op("Range", size, hi_end, step)

        low_size = sym_help._size_helper(g, low_indices, g.op("Constant", value_t=torch.tensor(0)))
        hi_size = sym_help._size_helper(g, hi_indices, g.op("Constant", value_t=torch.tensor(0)))

        ndim = sym_help._get_tensor_rank(input)
        perm = list(range(0, ndim))
        perm.append(perm.pop(dimension))

        unsqueeze_list = []
        loop_condition = g.op("Constant", value_t=torch.tensor(1))
        loop_condition = g.op("Cast", loop_condition, to_i=9)
        loop_len = g.op("Min", low_size, hi_size)
        loop = g.op("Loop", loop_len, loop_condition)

        loop_block = _add_block(loop.node())
        block_input_iter = _add_input_to_block(loop_block)
        cond = _add_input_to_block(loop_block)

        starts = loop_block.op("Gather", low_indices, block_input_iter)
        ends = loop_block.op("Gather", hi_indices, block_input_iter)
        axes = loop_block.op("Constant", value_t=torch.tensor([2]))
        starts = sym_help._unsqueeze_helper(loop_block, starts, [0])
        ends = sym_help._unsqueeze_helper(loop_block, ends, [0])
        stack = loop_block.op("Slice", input, starts, ends, axes)

        unsqueeze = sym_help._unsqueeze_helper(loop_block, loop_block.op("Transpose", stack, perm_i=perm), [dimension])
        unsqueeze_list.append(unsqueeze)
        concat = loop_block.op("Concat", *unsqueeze_list, axis_i=0)

        cond_out = loop_block.op("Cast", loop_condition, to_i=9)
        _add_output_to_block(loop_block, cond_out)
        _add_output_to_block(loop_block, concat)

        loop_output = loop.node().output()
        perm = [0, 1, 2, 3, 4]
        perm[0], perm[dimension + 1] = perm[dimension + 1], perm[0]
        transpose = g.op("Transpose", loop_output, perm_i=perm)
        squeeze = sym_help._squeeze_helper(g, transpose, [0])

        return squeeze
    else:
        return _unimplemented("Unfold", "input size not accessible")
