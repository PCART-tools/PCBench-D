def real(a: TensorLikeType) -> TensorLikeType:
    assert isinstance(a, TensorLike)
    if utils.is_complex_dtype(a.dtype):
        return prims.real(a)
    return a
