@register_decomposition([aten.upsample_linear1d.default, aten.upsample_linear1d.out])
@out_wrapper()
def upsample_linear1d(
    input: Tensor,
    output_size: list[int],
    align_corners: bool,
    scales_w: Optional[float] = None,
) -> Tensor:
    return _upsample_linear(input, output_size, align_corners, [scales_w])
