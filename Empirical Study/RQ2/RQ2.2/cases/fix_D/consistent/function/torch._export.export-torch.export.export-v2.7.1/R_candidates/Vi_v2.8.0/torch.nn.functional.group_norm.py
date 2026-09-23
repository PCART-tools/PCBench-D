def group_norm(
    input: Tensor,
    num_groups: int,
    weight: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    eps: float = 1e-5,
) -> Tensor:
    r"""Apply Group Normalization for last certain number of dimensions.

    See :class:`~torch.nn.GroupNorm` for details.
    """
    if has_torch_function_variadic(input, weight, bias):
        return handle_torch_function(
            group_norm,
            (
                input,
                weight,
                bias,
            ),
            input,
            num_groups,
            weight=weight,
            bias=bias,
            eps=eps,
        )
    if input.dim() < 2:
        raise RuntimeError(
            f"Expected at least 2 dimensions for input tensor but received {input.dim()}"
        )
    _verify_batch_size(
        [input.size(0) * input.size(1) // num_groups, num_groups]
        + list(input.size()[2:])
    )
    return torch.group_norm(
        input, num_groups, weight, bias, eps, torch.backends.cudnn.enabled
    )
