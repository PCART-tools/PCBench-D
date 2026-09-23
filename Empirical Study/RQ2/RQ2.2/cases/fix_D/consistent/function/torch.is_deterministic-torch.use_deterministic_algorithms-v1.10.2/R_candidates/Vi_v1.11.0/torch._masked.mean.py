@_apply_docstring_templates
def mean(input: Tensor,
         dim: DimOrDims = None,
         *,
         keepdim: Optional[bool] = False,
         dtype: Optional[DType] = None,
         mask: Optional[Tensor] = None) -> Tensor:
    """\
{reduction_signature}

{reduction_descr}

By definition, the identity value of a mean operation is the mean
value of the tensor. If all elements of the input tensor along given
dimension(s) :attr:`dim` are masked-out, the identity value of the
mean is undefined.  Due to this ambiguity, the elements of output
tensor with strided layout, that correspond to fully masked-out
elements, have ``nan`` values.

{reduction_args}

{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    if input.layout == torch.strided:
        inmask = _input_mask(input, mask=mask)
        count = sum(inmask.new_ones(input.shape, dtype=torch.int64), dim, keepdim=keepdim, mask=inmask)
        total = sum(input, dim, keepdim=keepdim, dtype=dtype, mask=inmask)
        return total / count
    else:
        raise ValueError(f'masked sum expects strided tensor (got {input.layout} tensor)')
