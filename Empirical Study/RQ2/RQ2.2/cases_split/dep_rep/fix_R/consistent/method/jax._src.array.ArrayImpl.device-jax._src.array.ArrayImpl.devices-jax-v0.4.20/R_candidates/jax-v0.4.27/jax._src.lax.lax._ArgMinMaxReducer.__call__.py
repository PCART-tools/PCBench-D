  def __call__(self, op_val_index, acc_val_index):
    op_val, op_index = op_val_index
    acc_val, acc_index = acc_val_index
    # Pick op_val if Lt (for argmin) or if NaN
    pick_op_val = bitwise_or(self._value_comparator(op_val, acc_val),
                             ne(op_val, op_val))
    # If x and y are not NaN and x = y, then pick the first
    pick_op_index = bitwise_or(pick_op_val,
                               bitwise_and(eq(op_val, acc_val),
                                           lt(op_index, acc_index)))
    return (select(pick_op_val, op_val, acc_val),
            select(pick_op_index, op_index, acc_index))
