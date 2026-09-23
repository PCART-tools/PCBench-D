def rprop(params: List[Tensor],
          grads: List[Tensor],
          prevs: List[Tensor],
          step_sizes: List[Tensor],
          *,
          step_size_min: float,
          step_size_max: float,
          etaminus: float,
          etaplus: float):
    r"""Functional API that performs rprop algorithm computation.

    See :class:`~torch.optim.Rprop` for details.
    """

    for i, param in enumerate(params):
        grad = grads[i]
        prev = prevs[i]
        step_size = step_sizes[i]

        sign = grad.mul(prev).sign()
        sign[sign.gt(0)] = etaplus
        sign[sign.lt(0)] = etaminus
        sign[sign.eq(0)] = 1

        # update stepsizes with step size updates
        step_size.mul_(sign).clamp_(step_size_min, step_size_max)

        # for dir<0, dfdx=0
        # for dir>=0 dfdx=dfdx
        grad = grad.clone(memory_format=torch.preserve_format)
        grad[sign.eq(etaminus)] = 0

        # update parameters
        param.addcmul_(grad.sign(), step_size, value=-1)

        prev.copy_(grad)
