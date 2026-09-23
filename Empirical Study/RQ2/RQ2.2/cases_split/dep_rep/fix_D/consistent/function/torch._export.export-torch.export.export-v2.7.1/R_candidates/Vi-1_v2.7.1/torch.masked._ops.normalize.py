@_apply_docstring_templates
def normalize(
    input: Union[Tensor, MaskedTensor],
    ord: float,
    dim: int,
    *,
    eps: float = 1e-12,
    dtype: Optional[DType] = None,
    mask: Optional[Tensor] = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    # TODO: eliminate mask_input as unnecessary when using masked divide.
    mask_input = _combine_input_and_mask(sum, input, mask)
    if mask_input.layout == torch.strided:
        nrm_ = norm(input, ord, dim, keepdim=True, dtype=dtype, mask=mask)
        # TODO: replace torch.maximum with masked maximum when available.
        denom = torch.maximum(nrm_, nrm_.new_full([], eps))
        # TODO: replace torch.divide with masked divide when available.
        return torch.divide(mask_input, denom)
    else:
        raise ValueError(
            f"masked normalize expects strided tensor (got {mask_input.layout} tensor)"
        )
