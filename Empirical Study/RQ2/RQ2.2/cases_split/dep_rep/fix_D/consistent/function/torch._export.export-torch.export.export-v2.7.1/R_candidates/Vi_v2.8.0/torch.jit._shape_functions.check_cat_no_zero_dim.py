def check_cat_no_zero_dim(tensors: list[list[int]]):
    for tensor in tensors:
        assert len(tensor) > 0
