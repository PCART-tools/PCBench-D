def _single_tensor_sgd(
    params: list[Tensor],
    grads: list[Tensor],
    momentum_buffer_list: list[Optional[Tensor]],
    grad_scale: Optional[Tensor],
    found_inf: Optional[Tensor],
    *,
    weight_decay: float,
    momentum: float,
    lr: float,
    dampening: float,
    nesterov: bool,
    maximize: bool,
    has_sparse_grad: bool,
):
    assert grad_scale is None and found_inf is None

    if not torch.jit.is_scripting():
        lr = _to_scalar(lr)

    for i, param in enumerate(params):
        grad = grads[i] if not maximize else -grads[i]

        if weight_decay != 0:
            # Nested if is necessary to bypass jitscript rules
            if isinstance(weight_decay, Tensor):
                if weight_decay.requires_grad:
                    # usually this is the differentiable path, which is why the param.clone() is needed
                    grad = grad.addcmul_(param.clone(), weight_decay)
                else:
                    grad = grad.add(param, alpha=weight_decay)
            else:
                grad = grad.add(param, alpha=weight_decay)

        if momentum != 0:
            buf = momentum_buffer_list[i]

            if buf is None:
                buf = torch.clone(grad).detach()
                momentum_buffer_list[i] = buf
            else:
                buf.mul_(momentum).add_(grad, alpha=1 - dampening)

            if nesterov:
                grad = grad.add(buf, alpha=momentum)
            else:
                grad = buf

        # Nested if is necessary to bypass jitscript rules
        if isinstance(lr, Tensor):
            if lr.requires_grad:
                param.addcmul_(grad, lr, value=-1)
            else:
                param.add_(grad, alpha=-lr)
        else:
            param.add_(grad, alpha=-lr)
