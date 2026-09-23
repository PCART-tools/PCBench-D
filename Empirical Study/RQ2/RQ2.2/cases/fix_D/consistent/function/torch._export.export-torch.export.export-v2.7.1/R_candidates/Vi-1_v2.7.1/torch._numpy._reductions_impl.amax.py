@_deco_axis_expand
def amax(
    a: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    keepdims: KeepDims = False,
    initial: NotImplementedType = None,
    where: NotImplementedType = None,
):
    if a.is_complex():
        raise NotImplementedError(f"amax with dtype={a.dtype}")

    return a.amax(axis)
