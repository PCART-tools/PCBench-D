@_apply_docstring_templates
def var(input: Tensor,
        dim: DimOrDims = None,
        unbiased: Optional[bool] = False,
        *,
        keepdim: Optional[bool] = False,
        dtype: Optional[DType] = None,
        mask: Optional[Tensor] = None) -> Tensor:
    """\
{reduction_signature}

{reduction_descr}

The identity value of sample variance operation is undefined.  The
elements of output tensor with strided layout, that correspond to
fully masked-out elements, have ``nan`` values.

{reduction_args}

{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
        if not (dtype.is_floating_point or dtype.is_complex):
            dtype = torch.float32
    compute_dtype = dtype
    if not (compute_dtype.is_floating_point or compute_dtype.is_complex):
        compute_dtype = torch.float32
    if input.layout == torch.strided:
        inmask = _input_mask(input, mask=mask)
        count = sum(inmask.new_ones(input.shape, dtype=torch.int64), dim, keepdim=True, mask=inmask)
        sample_total = sum(input, dim, keepdim=True, dtype=dtype, mask=inmask)
        # TODO: replace torch.subtract/divide/square/maximum with
        # masked subtract/divide/square/maximum when these will be
        # available.
        sample_mean = torch.divide(sample_total, count)
        x = torch.subtract(input, sample_mean)
        total = sum(x * x.conj(), dim, keepdim=keepdim, dtype=compute_dtype, mask=inmask)
        if not keepdim:
            count = count.reshape(total.shape)
        if unbiased:
            count = torch.subtract(count, 1)
            count = torch.maximum(count, count.new_zeros([]))
        return torch.divide(total, count).to(dtype=dtype)
    else:
        raise ValueError(f'masked var expects strided tensor (got {input.layout} tensor)')
