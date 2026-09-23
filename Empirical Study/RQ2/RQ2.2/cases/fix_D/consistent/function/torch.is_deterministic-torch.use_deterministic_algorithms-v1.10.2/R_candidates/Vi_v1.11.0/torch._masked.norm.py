@_apply_docstring_templates
def norm(input: Tensor,
         ord: Optional[float] = 2.0,
         dim: DimOrDims = None,
         *,
         keepdim: Optional[bool] = False,
         dtype: Optional[DType] = None,
         mask: Optional[Tensor] = None) -> Tensor:
    """\
{reduction_signature}

{reduction_descr}

The identity value of norm operation, which is used to start the
reduction, is ``{identity_float32}``, except for ``ord=-inf`` it is
``{identity_ord_ninf}``.

{reduction_args}

{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    if input.layout == torch.strided:
        identity = input.new_full([], _reduction_identity('norm', input, ord))
        mask_input = input if mask is None else torch.where(mask, input, identity)
        dim_ = _canonical_dim(dim, input.ndim)
        return torch.linalg.vector_norm(mask_input, ord, dim_, bool(keepdim), dtype=dtype)
    else:
        raise ValueError(f'masked norm expects strided tensor (got {input.layout} tensor)')
