def asgd(params: List[Tensor],
         grads: List[Tensor],
         axs: List[Tensor],
         mus: List[float],
         etas: List[float],
         *,
         weight_decay: float,
         lambd: float):
    r"""Functional API that performs asgd algorithm computation.

    See :class:`~torch.optim.ASGD` for details.
    """

    for i, param in enumerate(params):
        grad = grads[i]
        mu = mus[i]
        ax = axs[i]
        eta = etas[i]

        if weight_decay != 0:
            grad = grad.add(param, alpha=weight_decay)

        # decay term
        param.mul_(1 - lambd * eta)

        # update parameter
        param.add_(grad, alpha=-eta)

        # averaging
        if mu != 1:
            ax.add_(param.sub(ax).mul(mu))
        else:
            ax.copy_(param)
