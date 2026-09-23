def fill_(a: TensorLikeType, value: NumberType) -> TensorLikeType:
    r = prims.fill(a, value)
    prims.copy_to(a, r)
    return a
