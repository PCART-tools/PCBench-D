def get_gradient_edge(tensor: torch.Tensor) -> GradientEdge:
    """Get the gradient edge for computing the gradient of the given Tensor.

    In particular, it is equivalent to call
    ``g = autograd.grad(loss, input)`` and ``g = autograd.grad(loss, get_gradient_edge(input))``.
    """
    if not tensor.requires_grad:
        raise RuntimeError(
            "It is not possible to get the gradient edge for a Tensor "
            "that does not require gradients",
        )
    grad_fn = _get_grad_fn_or_grad_acc(tensor)

    # Note that output_nr default to 0 which is the right value
    # for the AccumulateGrad node.
    return GradientEdge(grad_fn, tensor.output_nr)
