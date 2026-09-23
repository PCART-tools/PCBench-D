@register_lowering(aten._upsample_nearest_exact3d.default)
def _upsample_nearest_exact3d(
    x,
    output_size,
    scales_d: Optional[float] = None,
    scales_h: Optional[float] = None,
    scales_w: Optional[float] = None,
):
    return upsample_nearestnd(
        x, output_size, (scales_d, scales_h, scales_w), n=3, exact=True
    )
