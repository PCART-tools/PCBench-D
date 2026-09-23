@parse_args("v", "i", "i", "i")
def diagonal(g, self, offset, dim1, dim2):
    dim1_size = size(g, self, dim=g.op("Constant", value_t=torch.LongTensor([dim1])))
    dim2_size = size(g, self, dim=g.op("Constant", value_t=torch.LongTensor([dim2])))

    # Create appropriate mask
    mask_shape = g.op("Concat", dim1_size, dim2_size, axis_i=0)
    mask = zeros(g, mask_shape, None, None, None)
    mask = g.op("EyeLike", mask, k_i=offset)

    # dim1 and dim2 appended as a dimension at the end of the shape
    rank = sym_help._get_tensor_rank(self)
    if rank is not None:
        axes = list(range(rank))
        axes.remove(dim1)
        axes.remove(dim2)
        self = g.op("Transpose", self, perm_i=axes + [dim1, dim2])
    else:
        return _unimplemented("diagonal", "unknown input rank")

    # Multiply input and mask to calculate values along diagonal
    # The mask consists of one values where diagonal values are to be calculated
    # For example:
    # [[1.1, 1.2, 1.3],   *    [[1, 0, 0]   =   [[1.1, 0, 0],
    #  [2.1, 2.2, 2.3],         [0, 1, 0]        [0, 2.2, 0],
    #  [3.1, 3.2, 3.3]]         [0, 0, 1]]       [0, 0, 3.3]]
    result = g.op("Mul", self, mask)
    result = sym_help._reducesum_helper(g, result, axes_i=[-1], keepdims_i=0)

    # Calculate gather indices based on offset and dims
    # If offset is greater than zero, set offset to zero as this aids in
    # calculation of selection window
    offset_op = g.op("Constant", value_t=torch.LongTensor([offset]))
    if offset >= 0:
        diag_size = g.op("Max", g.op("Min", dim1_size, g.op("Sub", dim2_size, offset_op)),
                         g.op("Constant", value_t=torch.LongTensor([0])))
        offset = 0
    else:
        diag_size = g.op("Max", g.op("Min", g.op("Add", dim1_size, offset_op), dim2_size),
                         g.op("Constant", value_t=torch.LongTensor([0])))
    diag_size = g.op("Concat", diag_size, axis_i=0)

    # Calculate which diagonal values to select
    # For example, in cases with offsets:
    # [[0, 1.1, 0]
    #  [0, 0, 2.2]]
    # we need to select the last two columns, so we create a tensor
    # with all columns that are to be selected
    # So in this example, it is [1, 2]
    select_window_ones_fill = ones(g, diag_size, 4, None, None)
    select_window = g.op("CumSum", select_window_ones_fill, g.op("Constant", value_t=torch.LongTensor([0])))
    select_window = g.op("Add", select_window, g.op("Constant", value_t=torch.LongTensor([abs(offset) - 1])))

    gather_shape = [size(g, result,
                         dim=g.op("Constant", value_t=torch.LongTensor([axis]))) for axis in list(range(rank))[:-2]]
    gather_shape.append(diag_size)
    gather_shape = g.op("Concat", *gather_shape, axis_i=0)
    gather_indices = zeros(g, gather_shape, 4, None, None)

    # There might be cases where offset value is greater than number of rows/columns
    # and might cause the diagonal to overrun and as a result of this, diag_size would be zero.
    # For example, if
    #       offset = 9, dim1_size = 2 (columns), dim2_size = 4 (rows)
    #       diag_size = max(min(2, (4-9)), 0) = 0, based on calculation above
    # Cases with diagonal overrun always result in diag_size = max(0, -ve value) = 0
    # In cases without diagonal overrun, we select the appropriate rows/columns along which we
    # are calculating diagonal values. In cases with diagonal overrun, we return a tensor which has
    # the dimension of the row/column where overrun occurred as 0-dim, as we are essentially
    # returning an empty tensor
    overrun_cond = g.op("Not", g.op("Equal", diag_size, g.op("Constant", value_t=torch.tensor(0, dtype=torch.int64))))
    if_op = g.op("If", overrun_cond)
    if_node = if_op.node()

    if_block = _add_block(if_node)
    gather_indices_if_block = if_block.op("Add", gather_indices, select_window)
    gather_indices_if_block = sym_help._unsqueeze_helper(if_block, gather_indices_if_block, [rank - 1])
    final_non_overrun_ = if_block.op("GatherND", result, gather_indices_if_block, batch_dims_i=rank - 2)
    _add_output_to_block(if_block, final_non_overrun_)

    else_block = _add_block(if_node)
    final_overrun_ = zeros(else_block, gather_shape, 6, None, None)
    _add_output_to_block(else_block, final_overrun_)
    return if_op
