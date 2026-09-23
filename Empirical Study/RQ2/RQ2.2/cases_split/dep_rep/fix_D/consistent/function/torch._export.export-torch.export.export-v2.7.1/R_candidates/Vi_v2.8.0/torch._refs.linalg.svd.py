@out_wrapper("U", "S", "Vh", exact_dtype=True)
def svd(A: TensorLikeType, full_matrices: bool = True) -> tuple[Tensor, Tensor, Tensor]:
    return prims.svd(A, full_matrices=full_matrices)
