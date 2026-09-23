@_deco_axis_expand
def ptp(
    a: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    keepdims: KeepDims = False,
):
    return a.amax(axis) - a.amin(axis)
