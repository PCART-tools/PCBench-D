def should_decompose_mm(mat1, mat2) -> bool:
    if is_node_meta_valid(mat1) and is_node_meta_valid(mat2):
        mat1 = mat1.meta["val"]
        mat2 = mat2.meta["val"]
    else:
        return False
    if len(mat1.shape) != 2 or len(mat2.shape) != 2:
        return False
    return (
        check_device(mat1, mat2, device="cuda")
        and mat1.shape[0] >= min_first_dimension_decomposition
        and mat2.shape[0] < max_other_dimention_decomposition
        and mat2.shape[1] < max_other_dimention_decomposition
    ) or (
        check_device(mat1, mat2, device="cpu")
        and mat1.shape[0] == 1
        and mat2.shape[0] <= 64
        and mat2.shape[1] <= 512
    )
