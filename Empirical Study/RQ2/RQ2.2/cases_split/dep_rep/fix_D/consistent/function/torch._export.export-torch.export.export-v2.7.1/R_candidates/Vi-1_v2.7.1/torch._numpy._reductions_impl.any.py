@_deco_axis_expand
def any(
    a: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    keepdims: KeepDims = False,
    *,
    where: NotImplementedType = None,
):
    axis = _util.allow_only_single_axis(axis)
    axis_kw = {} if axis is None else {"dim": axis}
    return torch.any(a, **axis_kw)
