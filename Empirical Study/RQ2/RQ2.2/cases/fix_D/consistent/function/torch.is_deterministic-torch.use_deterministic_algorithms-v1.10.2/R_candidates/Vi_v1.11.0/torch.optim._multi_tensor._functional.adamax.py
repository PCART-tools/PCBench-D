def adamax(params: List[Tensor],
           grads: List[Tensor],
           exp_avgs: List[Tensor],
           exp_infs: List[Tensor],
           states: List[Dict],
           *,
           beta1: float,
           beta2: float,
           lr: float,
           weight_decay: float,
           eps: float):
    r"""Functional API that performs Adamax algorithm computation.

    See :class:`~torch.optim.Adamax` for details.
    """

    if weight_decay != 0:
        torch._foreach_add_(grads, params, alpha=weight_decay)

    # Update biased first moment estimate.
    torch._foreach_mul_(exp_avgs, beta1)
    torch._foreach_add_(exp_avgs, grads, alpha=1 - beta1)

    # Update the exponentially weighted infinity norm.
    torch._foreach_mul_(exp_infs, beta2)

    for exp_inf, grad in zip(exp_infs, grads):
        norm_buf = torch.cat([
            exp_inf.unsqueeze(0),
            grad.abs().add_(eps).unsqueeze_(0)
        ], 0)
        torch.max(norm_buf, 0, keepdim=False, out=(exp_inf, exp_inf.new().long()))

    bias_corrections = [1 - beta1 ** state['step'] for state in states]
    clr = [-1 * (lr / bias_correction) for bias_correction in bias_corrections]
    torch._foreach_addcdiv_(params, exp_avgs, exp_infs, clr)
