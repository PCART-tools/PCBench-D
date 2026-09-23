@register_lowering(aten.upsample_nearest1d.default)
def upsample_nearest1d(x, output_size, scales: Optional[float] = None):
    return upsample_nearestnd(x, output_size, (scales,), n=1)
