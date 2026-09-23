def group_norm(
    input: Tensor,
    num_groups: int,
    weight: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    eps: float = 1e-5,
) -> Tensor:
    """
    Reference implementation of :func:`torch.nn.functional.group_norm`.
    """
    torch._check(
        input.ndim >= 2,
        lambda: f"Expected at least 2 dimensions for input tensor but received {input.ndim}",
    )

    batch_size = input.shape[0]
    num_channels = input.shape[1]
    torch._check(
        num_channels % num_groups == 0,
        lambda: "Expected number of channels in input to be divisible by num_groups, "
        + f"but got input of shape {input.shape} and num_groups = {num_groups}",
    )

    # input shape is (N, C, *), so we flatten all inner dimensions except (N, C)
    flattened_inner_size = 1
    for dim_length in input.shape[2:]:
        flattened_inner_size *= dim_length

    return torch.native_group_norm(
        input,
        weight,
        bias,
        batch_size,
        num_channels,
        flattened_inner_size,
        num_groups,
        eps,
    )[0]
