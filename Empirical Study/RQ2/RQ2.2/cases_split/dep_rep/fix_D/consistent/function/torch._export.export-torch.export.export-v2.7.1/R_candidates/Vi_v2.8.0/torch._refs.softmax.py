@out_wrapper()
def softmax(
    a: TensorLikeType,
    dim: int,
    dtype: Optional[torch.dtype] = None,
) -> TensorLikeType:
    result_dtype = dtype or a.dtype
    computation_dtype = utils.get_computation_dtype(result_dtype)
    a_ = _maybe_convert_to_dtype(a, computation_dtype)
    if a.numel() == 0:
        a_exp = exp(a_)
    else:
        a_max = amax(a_, dim, keepdim=True)
        a_exp = exp(a_ - a_max)
    return _maybe_convert_to_dtype(
        true_divide(a_exp, sum(a_exp, dim, keepdim=True)), result_dtype
    )  # type: ignore[return-value]
