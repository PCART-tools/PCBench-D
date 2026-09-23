def tensors1d(n, min_len=1, max_len=64, dtype=np.float32, elements=None):
    return tensors(
        n, 1, 1, dtype, elements, min_value=min_len, max_value=max_len
    )
