@_apply_docstring_templates
def argmin(
    input: Union[Tensor, MaskedTensor],
    dim: Optional[int] = None,
    *,
    keepdim: Optional[bool] = False,
    dtype: Optional[DType] = None,
    mask: Optional[Tensor] = None,
) -> Tensor:
    """\
{reduction_signature}
{reduction_descr}
{reduction_identity_dtype}
{reduction_args}
{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    mask_input = _combine_input_and_mask(argmin, input, mask)
    if mask_input.layout == torch.strided:
        return torch.argmin(mask_input, dim, bool(keepdim)).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked argmin expects strided tensor (got {mask_input.layout} tensor)"
        )
