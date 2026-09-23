def ravel(a: TensorLikeType) -> TensorLikeType:
    return reshape(a, (-1,))
