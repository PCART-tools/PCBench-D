@register_lowering(aten._upsample_nearest_exact1d.default)
def _upsample_nearest_exact1d(x, output_size, scales: Optional[float] = None):
    return upsample_nearestnd(x, output_size, (scales,), n=1, exact=True)
