@_deco_axis_expand
def amin(
    a: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    keepdims: KeepDims = False,
    initial: NotImplementedType = None,
    where: NotImplementedType = None,
):
    if a.is_complex():
        raise NotImplementedError(f"amin with dtype={a.dtype}")

    return a.amin(axis)
