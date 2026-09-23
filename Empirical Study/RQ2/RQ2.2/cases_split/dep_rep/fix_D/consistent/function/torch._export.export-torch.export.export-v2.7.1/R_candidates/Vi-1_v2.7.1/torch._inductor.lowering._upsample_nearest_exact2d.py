@register_lowering(aten._upsample_nearest_exact2d.default)
def _upsample_nearest_exact2d(
    x, output_size, scales_h: Optional[float] = None, scales_w: Optional[float] = None
):
    return upsample_nearestnd(x, output_size, (scales_h, scales_w), n=2, exact=True)
