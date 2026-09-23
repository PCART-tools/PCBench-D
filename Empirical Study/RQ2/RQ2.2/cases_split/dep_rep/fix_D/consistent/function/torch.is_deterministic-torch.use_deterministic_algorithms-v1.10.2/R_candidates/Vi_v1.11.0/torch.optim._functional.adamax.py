def adamax(params: List[Tensor],
           grads: List[Tensor],
           exp_avgs: List[Tensor],
           exp_infs: List[Tensor],
           state_steps: List[int],
           *,
           eps: float,
           beta1: float,
           beta2: float,
           lr: float,
           weight_decay: float):
    r"""Functional API that performs adamax algorithm computation.

    See :class:`~torch.optim.Adamax` for details.
    """

    for i, param in enumerate(params):
        grad = grads[i]
        exp_avg = exp_avgs[i]
        exp_inf = exp_infs[i]
        step = state_steps[i]

        if weight_decay != 0:
            grad = grad.add(param, alpha=weight_decay)

        # Update biased first moment estimate.
        exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
        # Update the exponentially weighted infinity norm.
        norm_buf = torch.cat([
            exp_inf.mul_(beta2).unsqueeze(0),
            grad.abs().add_(eps).unsqueeze_(0)
        ], 0)
        torch.amax(norm_buf, 0, keepdim=False, out=exp_inf)

        bias_correction = 1 - beta1 ** step
        clr = lr / bias_correction

        param.addcdiv_(exp_avg, exp_inf, value=-clr)
