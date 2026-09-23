def imag(a: TensorLikeType) -> TensorLikeType:
    assert isinstance(a, TensorLike)
    torch._check(
        utils.is_complex_dtype(a.dtype), lambda: "imag only supports complex tensors."
    )
    return prims.imag(a)
