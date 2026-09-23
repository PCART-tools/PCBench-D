@register_decomposition(
    [aten.upsample_bilinear2d.default, aten.upsample_bilinear2d.out]
)
@aten.upsample_bilinear2d.default.py_impl(DispatchKey.Autograd)
@out_wrapper()
def upsample_bilinear2d(
    input: Tensor,
    output_size: list[int],
    align_corners: bool,
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
) -> Tensor:
    return _upsample_linear(input, output_size, align_corners, [scales_h, scales_w])
