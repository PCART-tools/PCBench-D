def corrcoef(
    x: ArrayLike,
    y: Optional[ArrayLike] = None,
    rowvar=True,
    bias=None,
    ddof=None,
    *,
    dtype: Optional[DTypeLike] = None,
):
    if bias is not None or ddof is not None:
        # deprecated in NumPy
        raise NotImplementedError
    xy_tensor = _xy_helper_corrcoef(x, y, rowvar)

    is_half = (xy_tensor.dtype == torch.float16) and xy_tensor.is_cpu
    if is_half:
        # work around torch's "addmm_impl_cpu_" not implemented for 'Half'"
        dtype = torch.float32

    xy_tensor = _util.cast_if_needed(xy_tensor, dtype)
    result = torch.corrcoef(xy_tensor)

    if is_half:
        result = result.to(torch.float16)

    return result
