@register_lowering(aten.upsample_nearest2d.default)
def upsample_nearest2d(
    x, output_size, scales_h: Optional[float] = None, scales_w: Optional[float] = None
):
    return upsample_nearestnd(x, output_size, (scales_h, scales_w), n=2)
