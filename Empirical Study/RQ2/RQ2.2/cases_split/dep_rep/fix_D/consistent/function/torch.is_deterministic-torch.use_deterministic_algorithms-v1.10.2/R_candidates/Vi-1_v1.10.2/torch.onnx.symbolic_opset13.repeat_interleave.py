def repeat_interleave(g, self, repeats, dim=None, output_size=None):
    input = self
    final_dim = dim
    # if dim is None flatten
    # By default, use the flattened input array, and return a flat output array
    if sym_help._is_none(dim):
        input = sym_help._reshape_helper(g, self, g.op("Constant", value_t=torch.tensor([-1])))
        dim = 0
    else:
        dim = sym_help._maybe_get_scalar(dim)

    repeats_dim = sym_help._get_tensor_rank(repeats)
    repeats_sizes = sym_help._get_tensor_sizes(repeats)
    input_sizes = sym_help._get_tensor_sizes(input)
    if repeats_dim is None:
        raise RuntimeError("Unsupported: ONNX export of repeat_interleave for unknown "
                           "repeats rank.")
    if repeats_sizes is None:
        raise RuntimeError("Unsupported: ONNX export of repeat_interleave for unknown "
                           "repeats size.")
    if input_sizes is None:
        raise RuntimeError("Unsupported: ONNX export of repeat_interleave for unknown "
                           "input size.")
    # Handle cases where dim is negative
    if dim < 0:
        dim += len(input_sizes)

    output_sizes = input_sizes.copy()
    for idx, input_size in enumerate(input_sizes):
        if input_size is None:
            output_sizes[idx], input_sizes[idx] = 0, -1
    print(output_sizes, input_sizes)

    cond_dynamic_repeats = (repeats_dim == 1 and repeats_sizes[0] is None)
    # If input size is dynamic or repeats vector is dynamic
    if output_sizes[dim] == 0 or cond_dynamic_repeats:
        reps = sym_help._size_helper(g, input, dim)
        reps = unsqueeze(g, reps, 0)
        # Check if repeats vector is a single integer value
        # or a single dimension tensor with non-dynamic values
        if repeats_dim == 0 or (repeats_dim == 1 and repeats_sizes[0] == 1):
            if not sym_help._is_tensor(repeats):
                repeats = g.op("Constant", value_t=torch.LongTensor(repeats))
            repeats = g.op("Expand", repeats, reps)
        # Check if repeats is dynamic
        # As repeats is dynamic, we use a where node as a substitute for the if statement
        # If repests_dim = 1, expand repeats otherwise use original tensor
        elif cond_dynamic_repeats:
            repeat_dim = sym_help._size_helper(g, repeats, g.op("Constant", value_t=torch.LongTensor([0])))
            repeat_cond = g.op("Equal", repeat_dim, g.op("Constant", value_t=torch.LongTensor([1])))
            repeats = where(g, repeat_cond, g.op("Expand", repeats, reps), repeats)
    # There are cases when the repeats are 1-d tensor with multiple repeats, but dim
    # provided along one of the dynamic axes provided. A simple example would be
    # input.shape -> [1, 1, *] where * represents the dynamic axes, and dim = 2
    # Now, repeat interleaving can be performed in pytorch when the value of * matches
    # with the number of elements in repeat, for example if * -> 2, number of repeats
    # should be 2 as well.
    else:
        return torch.onnx.symbolic_opset9.repeat_interleave(g, self, repeats, final_dim)

    reps_like = g.op("ConstantOfShape", g.op("Shape", repeats),
                     value_t=torch.tensor([1], dtype=torch.long))
    r_splits = split(g, repeats, reps_like, 0)
    i_splits = split(g, input, reps_like, dim)

    output_sizes[dim], input_sizes[dim] = -1, 1

    # Create a loop to iterate over each value along the dimension
    # and perform individual interleaving using the repeats tensor
    # Loop is of the following pattern
    # input (trip_count, cond)
    #   int trip_count = ...;
    #   bool cond = ...;
    #   for (int i=0; i < trip_count && cond; ++i) {
    #     cond = ...;
    #   }

    # Loop conditions
    loop_condition = g.op("Constant", value_t=torch.tensor(1))
    loop_condition = g.op("Cast", loop_condition, to_i=9)
    loop_len = reps

    # Create an empty sequence to store final expansions
    final_splits = g.op("SequenceEmpty")
    loop = g.op("Loop", loop_len, loop_condition, final_splits)

    # Loop inputs
    loop_block = _add_block(loop.node())
    block_input_iter = _add_input_to_block(loop_block)
    cond = _add_input_to_block(loop_block)
    final_splits = _add_input_to_block(loop_block)

    r_split = loop_block.op("SequenceAt", r_splits, block_input_iter)
    i_split = loop_block.op("SequenceAt", i_splits, block_input_iter)

    i_split = unsqueeze(loop_block, i_split, dim + 1)
    r_concat = [loop_block.op("Constant", value_t=torch.LongTensor(input_sizes[:dim + 1])),
                r_split,
                loop_block.op("Constant", value_t=torch.LongTensor(input_sizes[dim + 1:]))]
    r_concat = loop_block.op("Concat", *r_concat, axis_i=0)
    i_split = expand(loop_block, i_split, r_concat, None)
    i_split = sym_help._reshape_helper(loop_block, i_split,
                                       g.op("Constant", value_t=torch.LongTensor(output_sizes)))
    final_splits = loop_block.op("SequenceInsert", final_splits, i_split)

    # Loop outputs
    cond_out = loop_block.op("Cast", loop_condition, to_i=9)
    _add_output_to_block(loop_block, cond_out)
    _add_output_to_block(loop_block, final_splits)

    loop_out = loop.node().output()
    loop_out = g.op("ConcatFromSequence", loop_out, axis_i=dim)
    return loop_out
