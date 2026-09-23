@register_meta(
    [
        aten.upsample_nearest2d_backward.default,
        aten._upsample_nearest_exact2d_backward.default,
    ]
)
def upsample_nearest2d_backward(
    grad_output: Tensor,
    output_size: Sequence[Union[int, torch.SymInt]],
    input_size: Sequence[Union[int, torch.SymInt]],
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
):
    full_output_size = upsample_common_check(
        input_size, output_size, num_spatial_dims=2
    )
    torch._check(
        grad_output.ndim == 4,
        lambda: f"Expected grad_output to be a tensor of dimension 4 but got: dimension {grad_output.ndim}",
    )
    for i in range(4):
        torch._check(
            grad_output.size(i) == full_output_size[i],
            lambda: (
                f"Expected grad_output to have the same shape as output;"
                f" output.size({i}) = {full_output_size[i]}"
                f" but got grad_output.size({i}) = {grad_output.size(i)}"
            ),
        )

    return grad_output.new_empty(input_size).to(
        memory_format=utils.suggest_memory_format(grad_output)
    )  # type: ignore[call-overload]
