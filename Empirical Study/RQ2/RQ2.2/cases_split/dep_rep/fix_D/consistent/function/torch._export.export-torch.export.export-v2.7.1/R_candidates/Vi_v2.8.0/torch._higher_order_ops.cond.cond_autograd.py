@cond_op.py_autograd_impl
def cond_autograd(pred, true_fn, false_fn, operands):
    return CondAutogradOp.apply(
        pred,
        true_fn,
        false_fn,
        *operands,
    )
