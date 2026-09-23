def ref_wngrad(param_in, seq_b_in, grad, lr, epsilon,
                output_effective_lr=False,
                output_effective_lr_and_update=False):
    # helper functions for wngrad operator test
    seq_b_out = seq_b_in + 1.0 / (seq_b_in + epsilon) * np.sum(grad * grad)
    effective_lr = lr / (seq_b_in + epsilon)
    grad_adj = effective_lr * grad
    param_out = param_in + grad_adj
    if output_effective_lr_and_update:
        return (param_out.astype(np.float32), seq_b_out.astype(np.float32),
                effective_lr.astype(np.float32),
                grad_adj.astype(np.float32))
    elif output_effective_lr:
        return (param_out.astype(np.float32), seq_b_out.astype(np.float32),
                effective_lr.astype(np.float32))
    return (param_out.astype(np.float32), seq_b_out.astype(np.float32))
