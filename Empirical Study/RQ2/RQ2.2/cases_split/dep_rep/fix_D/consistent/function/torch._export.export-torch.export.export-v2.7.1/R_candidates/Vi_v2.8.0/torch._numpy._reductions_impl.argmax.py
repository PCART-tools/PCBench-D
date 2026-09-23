@_deco_axis_expand
def argmax(
    a: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    *,
    keepdims: KeepDims = False,
):
    if a.is_complex():
        raise NotImplementedError(f"argmax with dtype={a.dtype}.")

    axis = _util.allow_only_single_axis(axis)

    if a.dtype == torch.bool:
        # RuntimeError: "argmax_cpu" not implemented for 'Bool'
        a = a.to(torch.uint8)

    return torch.argmax(a, axis)
