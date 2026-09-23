@cond_op.py_impl(DispatchKey.CompositeExplicitAutograd)
def cond_op_dense(pred, true_fn, false_fn, operands):
    assert all(
        isinstance(o, (torch.Tensor, int)) for o in operands
    ), f"Dense implementation operands must be a list of tensors and ints {operands}"
    mode = _get_current_dispatch_mode()
    assert mode is None, "Mode should never be enabled for CPU/CUDA key"
    if pred:
        return true_fn(*operands)
    else:
        return false_fn(*operands)
