@register_decomposition(aten.std)
@out_wrapper()
def std(
    a: TensorLikeType,
    dim: Union[Optional[int], Optional[list[int]]] = None,
    unbiased: Optional[bool] = None,
    keepdim: bool = False,
    *,
    correction: Optional[NumberType] = None,
) -> TensorLikeType:
    dim, unbiased = _dim_var_dispatch(dim, unbiased)
    correction = utils.set_correction(unbiased, correction)

    opmath_dtype, dtype = utils.reduction_dtypes(
        a, REDUCTION_OUTPUT_TYPE_KIND.COMPLEX_TO_FLOAT
    )
    a = _maybe_convert_to_dtype(a, opmath_dtype)
    a_var = torch.var(a, dim, correction=correction, keepdim=keepdim)
    a_std = torch.sqrt(a_var)
    assert dtype is not None
    return _maybe_convert_to_dtype(a_std, dtype)
