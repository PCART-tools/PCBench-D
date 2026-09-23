def _autograd_grad(outputs, inputs, grad_outputs=None, create_graph=False, retain_graph=None):
    # Version of autograd.grad that accepts `None` in outputs and do not compute gradients for them.
    # This has the extra constraint that inputs has to be a tuple
    assert isinstance(outputs, tuple)
    if grad_outputs is None:
        grad_outputs = (None,) * len(outputs)
    assert isinstance(grad_outputs, tuple)
    assert len(outputs) == len(grad_outputs)

    new_outputs: Tuple[torch.Tensor, ...] = tuple()
    new_grad_outputs: Tuple[torch.Tensor, ...] = tuple()
    for out, grad_out in zip(outputs, grad_outputs):
        if out is not None and out.requires_grad:
            new_outputs += (out,)
            new_grad_outputs += (grad_out,)

    if len(new_outputs) == 0:
        # No differentiable output, we don't need to call the autograd engine
        return (None,) * len(inputs)
    else:
        return torch.autograd.grad(new_outputs, inputs, new_grad_outputs, allow_unused=True,
                                   create_graph=create_graph, retain_graph=retain_graph)
