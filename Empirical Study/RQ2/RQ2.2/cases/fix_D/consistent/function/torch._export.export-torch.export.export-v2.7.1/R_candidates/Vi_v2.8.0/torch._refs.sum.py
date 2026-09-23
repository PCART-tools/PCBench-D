@register_decomposition([aten.sum.dim_IntList, aten.sum.IntList_out])
def sum(
    a: TensorLikeType,
    dim: Union[Optional[int], Optional[list[int]]] = None,
    keepdim: bool = False,
    *,
    dtype: Optional[torch.dtype] = None,
    out: Optional[Tensor] = None,
) -> TensorLikeType:
    if dtype is None:
        if out is not None:
            dtype = out.dtype
        elif utils.is_boolean_dtype(a.dtype) or utils.is_integer_dtype(a.dtype):
            dtype = torch.int64
        else:
            dtype = a.dtype
    # reduces over all dimensions if dim=() is passed
    if dim == () or dim == []:
        dim = None
    return _reduction(
        a,
        prims.sum,
        dims=dim,
        keepdims=keepdim,
        dtype=dtype,
        out=out,
        output_dtype_kind=REDUCTION_OUTPUT_TYPE_KIND.SAME,
    )
