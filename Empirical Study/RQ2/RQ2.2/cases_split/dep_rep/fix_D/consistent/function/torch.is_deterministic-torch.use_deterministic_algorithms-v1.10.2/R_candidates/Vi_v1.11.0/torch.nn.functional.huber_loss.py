def huber_loss(
    input: Tensor,
    target: Tensor,
    reduction: str = 'mean',
    delta: float = 1.0,
) -> Tensor:
    r"""Function that uses a squared term if the absolute
    element-wise error falls below delta and a delta-scaled L1 term otherwise.

    See :class:`~torch.nn.HuberLoss` for details.
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            huber_loss,
            (input, target),
            input,
            target,
            reduction=reduction,
            delta=delta,
        )
    if not (target.size() == input.size()):
        warnings.warn("Using a target size ({}) that is different to the input size ({}). "
                      "This will likely lead to incorrect results due to broadcasting. "
                      "Please ensure they have the same size.".format(target.size(), input.size()),
                      stacklevel=2)

    expanded_input, expanded_target = torch.broadcast_tensors(input, target)
    return torch._C._nn.huber_loss(expanded_input, expanded_target, _Reduction.get_enum(reduction), delta)
