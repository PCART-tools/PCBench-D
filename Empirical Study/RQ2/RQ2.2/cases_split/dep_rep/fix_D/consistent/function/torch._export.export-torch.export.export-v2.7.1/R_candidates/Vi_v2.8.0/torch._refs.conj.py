def conj(input: TensorLikeType) -> TensorLikeType:
    if not utils.is_complex_dtype(input.dtype):
        return input
    if input.is_sparse:
        return torch.conj_physical(input)
    return prims.conj(input)
