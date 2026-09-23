def cov(
    m: ArrayLike,
    y: Optional[ArrayLike] = None,
    rowvar=True,
    bias=False,
    ddof=None,
    fweights: Optional[ArrayLike] = None,
    aweights: Optional[ArrayLike] = None,
    *,
    dtype: Optional[DTypeLike] = None,
):
    m = _xy_helper_corrcoef(m, y, rowvar)

    if ddof is None:
        ddof = 1 if bias == 0 else 0

    is_half = (m.dtype == torch.float16) and m.is_cpu
    if is_half:
        # work around torch's "addmm_impl_cpu_" not implemented for 'Half'"
        dtype = torch.float32

    m = _util.cast_if_needed(m, dtype)
    result = torch.cov(m, correction=ddof, aweights=aweights, fweights=fweights)

    if is_half:
        result = result.to(torch.float16)

    return result
