def flipud(a: TensorLikeType) -> TensorLikeType:
    if a.ndim < 1:
        raise RuntimeError("Input must be >= 1-d.")

    return flip(a, (0,))
