@_apply_docstring_templates
def softmin(input: Tensor,
            dim: int,
            *,
            dtype: Optional[DType] = None,
            mask: Optional[Tensor] = None) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    if input.layout == torch.strided:
        fill = input.new_full([], _reduction_identity('amin', input))
        inmask = _input_mask(input, mask=mask)
        mask_input = torch.where(inmask, input, fill)
        return torch.nn.functional.softmin(mask_input, dim_, dtype=dtype)
    else:
        raise ValueError(f'masked softmin expects strided tensor (got {input.layout} tensor)')
