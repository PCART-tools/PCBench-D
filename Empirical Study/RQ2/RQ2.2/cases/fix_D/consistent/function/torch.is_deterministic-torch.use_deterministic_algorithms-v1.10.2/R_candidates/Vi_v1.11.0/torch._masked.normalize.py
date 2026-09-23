@_apply_docstring_templates
def normalize(input: Tensor,
              ord: float,
              dim: int,
              *,
              eps: float = 1e-12,
              dtype: Optional[DType] = None,
              mask: Optional[Tensor] = None) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    if input.layout == torch.strided:
        nrm_ = norm(input, ord, dim, keepdim=True, dtype=dtype, mask=mask)
        # TODO: replace torch.maximum with masked maximum when available.
        denom = torch.maximum(nrm_, nrm_.new_full([], eps))
        # TODO: eliminate mask_input as unnecessary when using masked divide.
        inmask = _input_mask(input, mask=mask)
        mask_input = input if mask is None else torch.where(inmask, input, input.new_zeros([]))
        # TODO: replace torch.divide with masked divide when available.
        return torch.divide(mask_input, denom)
    else:
        raise ValueError(f'masked normalize expects strided tensor (got {input.layout} tensor)')
