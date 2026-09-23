class _ArgMinMaxReducer:

  def __init__(self, value_comparator):
    self._value_comparator = value_comparator

  def __repr__(self):
    # Override the repr so that the metadata attached to the lowered op does not
    # contain unstable function ids. This plays more nicely with computation
    # fingerprint calculation in the compilation cache.
    return f'_ArgMinMaxReducer({self._value_comparator.__name__})'

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
