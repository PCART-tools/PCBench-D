@_apply_docstring_templates
def cumprod(
    input: Tensor,
    dim: int,
    *,
    dtype: Optional[DType] = None,
    mask: Optional[Tensor] = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    mask_input = _combine_input_and_mask(prod, input, mask)
    if mask_input.layout == torch.strided:
        return torch.cumprod(mask_input, dim_, dtype=dtype).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked cumprod expects strided tensor (got {mask_input.layout} tensor)"
        )
