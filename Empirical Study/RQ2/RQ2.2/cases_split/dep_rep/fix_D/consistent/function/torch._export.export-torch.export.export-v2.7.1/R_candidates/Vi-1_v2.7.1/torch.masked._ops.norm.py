@_apply_docstring_templates
def norm(
    input: Union[Tensor, MaskedTensor],
    ord: Optional[float] = 2.0,
    dim: DimOrDims = None,
    *,
    keepdim: Optional[bool] = False,
    dtype: Optional[DType] = None,
    mask: Optional[Tensor] = None,
) -> Tensor:
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
    mask_input = _combine_input_and_mask(norm, input, mask, ord)
    if mask_input.layout == torch.strided:
        dim_ = _canonical_dim(dim, input.ndim)
        return torch.linalg.vector_norm(
            mask_input, ord, dim_, bool(keepdim), dtype=dtype
        )
    else:
        raise ValueError(
            f"masked norm expects strided tensor (got {mask_input.layout} tensor)"
        )
