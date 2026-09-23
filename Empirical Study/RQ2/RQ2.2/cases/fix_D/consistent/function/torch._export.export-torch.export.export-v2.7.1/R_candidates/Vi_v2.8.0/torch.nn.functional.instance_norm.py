def instance_norm(
    input: Tensor,
    running_mean: Optional[Tensor] = None,
    running_var: Optional[Tensor] = None,
    weight: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    use_input_stats: bool = True,
    momentum: float = 0.1,
    eps: float = 1e-5,
) -> Tensor:
    r"""Apply Instance Normalization independently for each channel in every data sample within a batch.

    See :class:`~torch.nn.InstanceNorm1d`, :class:`~torch.nn.InstanceNorm2d`,
    :class:`~torch.nn.InstanceNorm3d` for details.
    """
    if has_torch_function_variadic(input, running_mean, running_var, weight, bias):
        return handle_torch_function(
            instance_norm,
            (input, running_mean, running_var, weight, bias),
            input,
            running_mean=running_mean,
            running_var=running_var,
            weight=weight,
            bias=bias,
            use_input_stats=use_input_stats,
            momentum=momentum,
            eps=eps,
        )
    if use_input_stats:
        _verify_spatial_size(input.size())
    return torch.instance_norm(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        use_input_stats,
        momentum,
        eps,
        torch.backends.cudnn.enabled,
    )
