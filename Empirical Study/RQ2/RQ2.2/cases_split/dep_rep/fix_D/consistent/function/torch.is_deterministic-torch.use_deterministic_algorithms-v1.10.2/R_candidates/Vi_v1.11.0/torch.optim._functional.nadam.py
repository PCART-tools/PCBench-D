def nadam(params: List[Tensor],
          grads: List[Tensor],
          exp_avgs: List[Tensor],
          exp_avg_sqs: List[Tensor],
          mu_products: List[float],
          state_steps: List[int],
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

    for i, param in enumerate(params):
        grad = grads[i]
        exp_avg = exp_avgs[i]
        exp_avg_sq = exp_avg_sqs[i]
        mu_product = mu_products[i]
        step = state_steps[i]

        bias_correction2 = 1 - beta2 ** step

        if weight_decay != 0:
            grad = grad.add(param, alpha=weight_decay)

        # calculate the momentum cache \mu^{t} and \mu^{t+1}
        mu = beta1 * (1. - 0.5 * (0.96 ** (step * momentum_decay)))
        mu_next = beta1 * (1. - 0.5 * (0.96 ** ((step + 1) * momentum_decay)))
        mu_product = mu_product * mu
        mu_product_next = mu_product * mu * mu_next

        # decay the first and second moment running average coefficient
        exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
        exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

        denom = exp_avg_sq.div(bias_correction2).sqrt().add_(eps)
        param.addcdiv_(grad, denom, value=-lr * (1. - mu) / (1. - mu_product))
        param.addcdiv_(exp_avg, denom, value=-lr * mu_next / (1. - mu_product_next))
