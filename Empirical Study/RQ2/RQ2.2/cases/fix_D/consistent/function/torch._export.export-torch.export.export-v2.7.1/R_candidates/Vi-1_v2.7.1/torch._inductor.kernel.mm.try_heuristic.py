def try_heuristic(m, n, k, choices, mat1, mat2, mat2_dtype, layout):
    m, n, k = get_size_hints(mat1, mat2, m, n, k)
    if not dims_are_int([m, n, k]):
        return None

    if mat1.dtype != torch.float16:
        return None

    # only use heuristic if we are running on an A100
    # torch.cuda.get_device_capability() >= (8, 0) returns true for A10G
    # which does not have enough shared memory for one of the configs
    if (
        not torch.cuda.get_device_capability() >= (8, 0)
    ) or get_gpu_shared_memory() != 166912:
        return None

    if m == 1 and (n % 16 != 0 or k % 16 != 0):
        return None

    if m <= 16 and n >= 4096 and k >= 4096:
        return triton_config(
            BLOCK_M=16,
            BLOCK_N=64,
            BLOCK_K=128,
            num_stages=5,
            num_warps=4,
        )
    elif m > 16 and m <= 32 and n >= 4096 and k >= 4096:
        return triton_config(
            BLOCK_M=32,
            BLOCK_N=32,
            BLOCK_K=128,
            num_stages=5,
            num_warps=4,
        )
    elif m > 32 and m <= 64 and n >= 4096 and k >= 4096:
        return triton_config(
            BLOCK_M=64,
            BLOCK_N=32,
            BLOCK_K=128,
            num_stages=5,
            num_warps=4,
        )
    return None
