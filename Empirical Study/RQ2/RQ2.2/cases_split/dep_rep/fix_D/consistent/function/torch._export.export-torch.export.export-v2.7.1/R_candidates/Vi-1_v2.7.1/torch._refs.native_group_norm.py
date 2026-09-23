@register_decomposition(aten.native_group_norm.default)
def native_group_norm(
    input: Tensor,
    weight: Optional[Tensor],
    bias: Optional[Tensor],
    batch_size: int,
    num_channels: int,
    flattened_inner_size: int,
    num_groups: int,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor]:
    torch._check(
        input.ndim >= 2,
        lambda: f"Expected at least 2 dimensions for input tensor but received {input.ndim}",
    )
    torch._check(
        num_channels % num_groups == 0,
        lambda: "Expected number of channels in input to be divisible by num_groups, "
        + f"but got input of shape {input.shape} and num_groups = {num_groups}",
    )

    # num_channels / num_groups and flattened inner dimension are the reduction axes
    reduction_dims = [2, 3]
    input_reshaped = torch.reshape(
        input,
        [batch_size, num_groups, num_channels // num_groups, flattened_inner_size],
    )
    out, mean, rstd = _normalize(input_reshaped, reduction_dims, eps)
    out = out.view(input.shape)

    broadcast_dims = [0] + list(range(2, input.ndim))
    unsqueeze_bias = None
    if bias is not None:
        unsqueeze_bias = _unsqueeze_multiple(bias, broadcast_dims)
    unsqueeze_weight = None
    if weight is not None:
        unsqueeze_weight = _unsqueeze_multiple(weight, broadcast_dims)

    if unsqueeze_weight is not None:
        out = out * unsqueeze_weight
    if unsqueeze_bias is not None:
        out = out + unsqueeze_bias

    out = _maybe_convert_to_dtype(out, input.dtype)  # type: ignore[assignment]
    mean = _maybe_convert_to_dtype(mean, input.dtype)  # type: ignore[assignment]
    rstd = _maybe_convert_to_dtype(rstd, input.dtype)  # type: ignore[assignment]

    # remove broadcast dimensions from mean and rstd
    mean = torch.squeeze(mean, reduction_dims)
    rstd = torch.squeeze(rstd, reduction_dims)
    return (out, mean, rstd)
