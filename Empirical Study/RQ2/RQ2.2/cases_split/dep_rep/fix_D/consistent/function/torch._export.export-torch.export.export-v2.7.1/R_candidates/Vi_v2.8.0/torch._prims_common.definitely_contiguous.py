def definitely_contiguous(a: TensorLikeType) -> bool:
    return is_contiguous(a, false_if_dde=True)
