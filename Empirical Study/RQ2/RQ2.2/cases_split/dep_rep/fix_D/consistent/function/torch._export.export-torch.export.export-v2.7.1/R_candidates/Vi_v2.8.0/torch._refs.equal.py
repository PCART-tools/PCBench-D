def equal(a: TensorLikeType, b: TensorLikeType) -> bool:
    utils.check_same_device(a, b, allow_cpu_scalar_tensors=False)
    utils.check_same_dtype(a, b)

    # Shape check
    if a.ndim != b.ndim:
        return False

    for x, y in zip(a.shape, b.shape):
        if x != y:
            return False

    # Short-circuits if there are no elements to validate
    if a.numel() == 0:
        return True

    return item(all(eq(a, b)))  # type: ignore[return-value]
