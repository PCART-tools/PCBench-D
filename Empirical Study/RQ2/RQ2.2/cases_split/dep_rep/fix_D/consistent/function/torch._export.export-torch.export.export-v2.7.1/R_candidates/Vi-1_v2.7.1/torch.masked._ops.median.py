@_apply_docstring_templates
def median(
    input: Union[Tensor, MaskedTensor],
    dim: int = -1,
    *,
    keepdim: bool = False,
    dtype: Optional[DType] = None,
    mask: Optional[Tensor] = None,
) -> Tensor:
    """\
{reduction_signature}
{reduction_descr}
By definition, the identity value of a median operation is the median
value of the tensor. If all elements of the input tensor along given
dimension(s) :attr:`dim` are masked-out, the identity value of the
median is undefined.  Due to this ambiguity, the elements of output
tensor with strided layout, that correspond to fully masked-out
elements, have ``nan`` values.
{reduction_args}
{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    is_float = torch.is_floating_point(input)
    if not is_float:
        input = input.to(dtype=torch.float)
    mask_input = _combine_input_and_mask(median, input, mask)
    if mask_input.layout == torch.strided:
        output = torch.nanmedian(mask_input, dim_, keepdim).values
        if is_float:
            return output
        elif not is_float and not torch.isnan(output).any():
            return output.to(dtype=dtype)
        else:
            raise ValueError(
                "masked median expects no fully masked out rows if dtype is not floating point"
            )
    else:
        raise ValueError(
            f"masked median expects strided tensor (got {mask_input.layout} tensor)"
        )
