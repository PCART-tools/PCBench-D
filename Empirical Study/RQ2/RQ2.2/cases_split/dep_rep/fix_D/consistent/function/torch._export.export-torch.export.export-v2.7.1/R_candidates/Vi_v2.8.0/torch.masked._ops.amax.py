@_apply_docstring_templates
def amax(
    input: Union[Tensor, MaskedTensor],
    dim: DimOrDims = None,
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

    mask_input = _combine_input_and_mask(amax, input, mask)
    dim_ = _canonical_dim(dim, mask_input.ndim)
    if mask_input.layout == torch.strided:
        return torch.amax(mask_input, dim_, bool(keepdim)).to(dtype=dtype)
    elif mask_input.layout == torch.sparse_coo:
        if mask is None:
            # See comment in the sparse_csr branch of prod, a similar issue arises here
            # where unspecified elements along a dimension may need to be reduced with the result
            raise ValueError(
                "masked amax expects explicit mask for sparse_coo tensor input"
            )
        return _sparse_coo_scatter_reduction_helper(
            torch.amax, mask_input, dim_, bool(keepdim), dtype
        )
    elif mask_input.layout == torch.sparse_csr:
        if mask is None:
            raise ValueError(
                "masked amax expects explicit mask for sparse_csr tensor input"
            )
        return _sparse_csr_segment_reduction_helper(
            torch.amax, mask_input, dim_, bool(keepdim), dtype
        )
    else:
        raise ValueError(
            f"masked amax expects strided, sparse_coo or sparse_csr tensor (got {mask_input.layout} tensor)"
        )
