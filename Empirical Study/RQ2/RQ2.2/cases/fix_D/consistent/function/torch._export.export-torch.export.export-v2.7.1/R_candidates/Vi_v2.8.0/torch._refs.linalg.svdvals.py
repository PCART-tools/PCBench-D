@out_wrapper(exact_dtype=True)
def svdvals(A: TensorLikeType) -> Tensor:
    return svd(A, full_matrices=False)[1]
