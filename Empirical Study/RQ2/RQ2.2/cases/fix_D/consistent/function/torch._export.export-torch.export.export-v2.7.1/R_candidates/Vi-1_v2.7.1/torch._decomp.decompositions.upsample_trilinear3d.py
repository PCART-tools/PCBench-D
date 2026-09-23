@register_decomposition(
    [aten.upsample_trilinear3d.default, aten.upsample_trilinear3d.out]
)
@out_wrapper()
def upsample_trilinear3d(
    input: Tensor,
    output_size: list[int],
    align_corners: bool,
    scales_d: Optional[float] = None,
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
) -> Tensor:
    return _upsample_linear(
        input, output_size, align_corners, [scales_d, scales_h, scales_w]
    )
