def should_decompose_bmm(mat1, mat2) -> bool:
    if is_node_meta_valid(mat1) and is_node_meta_valid(mat2):
        mat1 = mat1.meta["val"]
        mat2 = mat2.meta["val"]
    else:
        return False
    if len(mat1.shape) != 3 or len(mat2.shape) != 3:
        return False
    if check_device(mat1, mat2, device="cuda"):
        if mat1.shape[0] < min_first_dimension_decomposition:
            return False
        # 2 of m, n, k must be <= MAX_OTHER_DIMENSION_DECOMPOSITION
        if (mat1.shape[1] < max_other_dimention_decomposition) + (
            mat1.shape[2] < max_other_dimention_decomposition
        ) + (mat2.shape[2] < max_other_dimention_decomposition) < 2:
            return False
        return True
    elif check_device(mat1, mat2, device="cpu"):
        if mat1.shape[0] == 1 and mat2.shape[0] == 1:
            return True
    return False
