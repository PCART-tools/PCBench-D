@_apply_docstring_templates
def logsumexp(
    input: Tensor,
    dim: DimOrDims = None,
    *,
    keepdim: bool = False,
    dtype: Optional[DType] = None,
    mask: Optional[Tensor] = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)
    mask_input = _combine_input_and_mask(logsumexp, input, mask)
    if mask_input.layout == torch.strided:
        return torch.logsumexp(mask_input, dim_, keepdim=keepdim).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked logsumexp expects strided tensor (got {mask_input.layout} tensor)"
        )
