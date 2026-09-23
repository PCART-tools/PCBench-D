def adagrad(
    params: List[Tensor],
    grads: List[Tensor],
    state_sums: List[Tensor],
    state_steps: List[int],
    has_sparse_grad: bool,
    *,
    lr: float,
    weight_decay: float,
    lr_decay: float,
    eps: float
):
    r"""Functional API that performs Adagrad algorithm computation.

    See :class:`~torch.optim.Adagrad` for details.
    """

    if weight_decay != 0:
        if has_sparse_grad:
            raise RuntimeError(
                "weight_decay option is not compatible with sparse gradients"
            )
        torch._foreach_add_(grads, params, alpha=weight_decay)

    minus_clr = [-lr / (1 + (step - 1) * lr_decay) for step in state_steps]

    if has_sparse_grad:
        # sparse is not supported by multi_tensor. Fall back to optim.adagrad
        # implementation for sparse gradients
        for i, (param, grad, state_sum, step) in enumerate(
            zip(params, grads, state_sums, state_steps)
        ):
            grad = grad.coalesce()  # the update is non-linear so indices must be unique
            grad_indices = grad._indices()
            grad_values = grad._values()
            size = grad.size()

            state_sum.add_(_make_sparse(grad, grad_indices, grad_values.pow(2)))
            std_sparse = state_sum.sparse_mask(grad)
            std_sparse_values = std_sparse._values().sqrt_().add_(eps)
            param.add_(
                _make_sparse(grad, grad_indices, grad_values / std_sparse_values),
                alpha=minus_clr[i],
            )
    else:
        grads = [torch.view_as_real(x) if torch.is_complex(x) else x for x in grads]
        state_sums = [torch.view_as_real(x) if torch.is_complex(x) else x for x in state_sums]
        torch._foreach_addcmul_(state_sums, grads, grads, value=1)
        std = torch._foreach_add(torch._foreach_sqrt(state_sums), eps)
        toAdd = torch._foreach_div(torch._foreach_mul(grads, minus_clr), std)
        toAdd = [torch.view_as_complex(x) if torch.is_complex(params[i]) else x for i, x in enumerate(toAdd)]
        torch._foreach_add_(params, toAdd)
        state_sums = [torch.view_as_complex(x) if torch.is_complex(params[i]) else x for i, x in enumerate(state_sums)]
