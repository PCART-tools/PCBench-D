@_apply_docstring_templates
def argmax(
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
    mask_input = _combine_input_and_mask(argmax, input, mask)
    if mask_input.layout == torch.strided:
        return torch.argmax(mask_input, dim, bool(keepdim)).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked argmax expects strided tensor (got {mask_input.layout} tensor)"
        )
