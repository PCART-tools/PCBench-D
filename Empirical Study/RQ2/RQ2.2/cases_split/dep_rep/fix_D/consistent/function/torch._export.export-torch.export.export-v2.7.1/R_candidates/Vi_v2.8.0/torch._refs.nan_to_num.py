@register_decomposition(aten.nan_to_num)
@out_wrapper()
def nan_to_num(
    a: TensorLikeType,
    nan: Optional[NumberType] = 0.0,
    posinf: Optional[NumberType] = None,
    neginf: Optional[NumberType] = None,
) -> TensorLikeType:
    assert isinstance(a, TensorLike)

    if utils.is_boolean_dtype(a.dtype) or utils.is_integer_dtype(a.dtype):
        return a.clone()

    if nan is None:
        nan = 0.0

    if posinf is None:
        posinf = torch.finfo(a.dtype).max

    if neginf is None:
        neginf = torch.finfo(a.dtype).min

    result = torch.where(torch.isnan(a), nan, a)  # type: ignore[call-overload]
    result = torch.where(torch.isneginf(a), neginf, result)  # type: ignore[call-overload]
    result = torch.where(torch.isposinf(a), posinf, result)  # type: ignore[call-overload]
    return result
