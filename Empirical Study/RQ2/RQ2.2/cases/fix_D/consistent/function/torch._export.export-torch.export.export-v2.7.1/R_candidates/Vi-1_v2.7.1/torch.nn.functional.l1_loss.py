def l1_loss(
    input: Tensor,
    target: Tensor,
    size_average: Optional[bool] = None,
    reduce: Optional[bool] = None,
    reduction: str = "mean",
    weight: Optional[Tensor] = None,
) -> Tensor:  # noqa: D400,D402
    r"""l1_loss(input, target, size_average=None, reduce=None, reduction='mean') -> Tensor

    Function that takes the mean element-wise absolute value difference.

    See :class:`~torch.nn.L1Loss` for details.
    """
    if has_torch_function_variadic(input, target):
        return handle_torch_function(
            l1_loss,
            (input, target, weight),
            input,
            target,
            size_average=size_average,
            reduce=reduce,
            reduction=reduction,
        )
    if not (target.size() == input.size()):
        warnings.warn(
            f"Using a target size ({target.size()}) that is different to the input size ({input.size()}). "
            "This will likely lead to incorrect results due to broadcasting. "
            "Please ensure they have the same size.",
            stacklevel=2,
        )
    if size_average is not None or reduce is not None:
        reduction = _Reduction.legacy_get_string(size_average, reduce)

    expanded_input, expanded_target = torch.broadcast_tensors(input, target)

    if weight is not None:
        if weight.size() != input.size():
            raise ValueError("Weights and input must have the same size.")

        absolute_errors = torch.abs(expanded_input - expanded_target)
        weighted_absolute_errors = absolute_errors * weight

        if reduction == "none":
            return weighted_absolute_errors
        elif reduction == "sum":
            return torch.sum(weighted_absolute_errors)
        elif reduction == "mean":
            return torch.sum(weighted_absolute_errors) / torch.sum(weight)
        else:
            raise ValueError(
                f"Invalid reduction mode: {reduction}. Expected one of 'none', 'mean', 'sum'."
            )
    else:
        return torch._C._nn.l1_loss(
            expanded_input, expanded_target, _Reduction.get_enum(reduction)
        )
