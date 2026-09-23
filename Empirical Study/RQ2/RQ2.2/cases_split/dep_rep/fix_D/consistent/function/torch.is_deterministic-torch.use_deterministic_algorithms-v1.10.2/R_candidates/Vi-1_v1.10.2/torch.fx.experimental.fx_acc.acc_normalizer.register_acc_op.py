def register_acc_op(acc_op: Callable):
    """
    For a new acc op, add this as decorator to register it.
    """
    _acc_ops.add(acc_op)
    return acc_op
