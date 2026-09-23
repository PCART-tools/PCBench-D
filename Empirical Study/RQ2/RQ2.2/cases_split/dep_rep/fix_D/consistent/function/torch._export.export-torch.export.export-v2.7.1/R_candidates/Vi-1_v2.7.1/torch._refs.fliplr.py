def fliplr(a: TensorLikeType) -> TensorLikeType:
    if a.ndim < 2:
        raise RuntimeError("Input must be >= 2-d.")

    return flip(a, (1,))
