def nadam(params: List[Tensor],
          grads: List[Tensor],
          exp_avg: List[Tensor],
          exp_avg_sq: List[Tensor],
          mu_products: List[Tensor],
          states: List[Dict],
          *,
          beta1: float,
          beta2: float,
          lr: float,
          weight_decay: float,
          momentum_decay: float,
          eps: float):
    r"""Functional API that performs NAdam algorithm computation.

    See :class:`~torch.optim.NAdam` for details.
    """

    bias_correction1 = [1 - beta1 ** state['step'] for state in states]
    bias_correction2 = [1 - beta2 ** state['step'] for state in states]
    mus = [beta1 * (1. - 0.5 * (0.96 ** (state['step'] * momentum_decay))) for state in states]
    mu_nexts = [beta1 * (1. - 0.5 * (0.96 ** ((state['step'] + 1) * momentum_decay)))
                for state in states]
    if weight_decay != 0:
        torch._foreach_add_(grads, params, alpha=weight_decay)

    # Decay the first and second moment running average coefficient
    torch._foreach_mul_(exp_avg, beta1)
    torch._foreach_add_(exp_avg, grads, alpha=1 - beta1)

    torch._foreach_mul_(exp_avg_sq, beta2)
    torch._foreach_addcmul_(exp_avg_sq, grads, grads, 1 - beta2)

    exp_avg_sq_sqrt = torch._foreach_sqrt(exp_avg_sq)
    bias_correction_sqrt = [math.sqrt(bc) for bc in bias_correction2]
    torch._foreach_div_(exp_avg_sq_sqrt, bias_correction_sqrt)
    denom = torch._foreach_add(exp_avg_sq_sqrt, eps)

    step_size_grads = [(lr * (1. - mu) / (1. - mu_product)) * -1
                       for mu_product, mu in zip(mu_products, mus)]
    step_size_expavg = [(lr * mu_next / (1. - mu_product * mu_next)) * -1
                        for mu_product, mu_next in zip(mu_products, mu_nexts)]
    torch._foreach_addcdiv_(params, grads, denom, step_size_grads)
    torch._foreach_addcdiv_(params, exp_avg, denom, step_size_expavg)
