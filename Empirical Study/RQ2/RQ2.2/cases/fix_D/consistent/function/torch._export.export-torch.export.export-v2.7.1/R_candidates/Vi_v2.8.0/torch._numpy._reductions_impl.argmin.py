@_deco_axis_expand
def argmin(
    a: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    *,
    keepdims: KeepDims = False,
):
    if a.is_complex():
        raise NotImplementedError(f"argmin with dtype={a.dtype}.")

    axis = _util.allow_only_single_axis(axis)

    if a.dtype == torch.bool:
        # RuntimeError: "argmin_cpu" not implemented for 'Bool'
        a = a.to(torch.uint8)

    return torch.argmin(a, axis)
