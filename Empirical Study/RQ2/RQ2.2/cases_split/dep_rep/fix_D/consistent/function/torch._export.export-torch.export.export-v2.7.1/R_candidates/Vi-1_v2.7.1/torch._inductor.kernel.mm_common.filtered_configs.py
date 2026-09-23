def filtered_configs(
    m: int,
    n: int,
    k: int,
    configs: Sequence[tuple[int, int, int, int, int]],
    has_int8_tensor=False,
    scale=1,
    exclude=lambda m, n, k: False,
):
    """
    Heuristic to shrink configs when they are bigger than the input size

    :param scale: scale factor applied to the config values
    :param exclude: whether a given config should be excluded
    """
    from torch._inductor import config

    max_mm_configs = config.test_configs.max_mm_configs

    min_block_size = 16
    # block_k=16 seems to be causing issues
    # see: https://github.com/triton-lang/triton/issues/2156#issuecomment-1695897424
    min_block_size_k = 32 if has_int8_tensor else 16
    m = max(
        next_power_of_2(
            V.graph.sizevars.size_hint(
                m,
                fallback=torch._inductor.config.unbacked_symint_fallback,  # type: ignore[arg-type]
            )
        ),
        min_block_size,
    )
    n = max(
        next_power_of_2(
            V.graph.sizevars.size_hint(
                n,
                fallback=torch._inductor.config.unbacked_symint_fallback,  # type: ignore[arg-type]
            )
        ),
        min_block_size,
    )
    k = max(
        next_power_of_2(
            V.graph.sizevars.size_hint(
                k,
                fallback=torch._inductor.config.unbacked_symint_fallback,  # type: ignore[arg-type]
            )
        ),
        min_block_size_k,
    )
    used = OrderedSet[tuple[int, ...]]()
    for block_m, block_n, block_k, num_stages, num_warps in configs:
        # shrink configs for small sizes
        block_m = max(min(int(block_m * scale), m), min_block_size)
        block_n = max(min(int(block_n * scale), n), min_block_size)
        block_k = max(min(int(block_k * scale), k), min_block_size_k)

        if exclude(block_m, block_n, block_k):
            continue

        # each warp computes 16x16 tile = 256
        num_warps = min(num_warps, block_m * block_n // 256)
        if torch.version.hip:
            kpack = 2
            for matrix_instr_nonkdim in [0, 16]:
                if matrix_instr_nonkdim != 0 and (
                    block_m % matrix_instr_nonkdim != 0
                    or block_n % matrix_instr_nonkdim != 0
                ):
                    #  block_m and block_n must be a multiple of matrix_instr_nonkdim
                    continue

                if (
                    block_m,
                    block_n,
                    block_k,
                    num_stages,
                    num_warps,
                    matrix_instr_nonkdim,
                    kpack,
                ) not in used and (
                    max_mm_configs is None or len(used) < max_mm_configs
                ):
                    used.add(
                        (
                            block_m,
                            block_n,
                            block_k,
                            num_stages,
                            num_warps,
                            matrix_instr_nonkdim,
                            kpack,
                        )
                    )
                    yield triton_config(
                        BLOCK_M=block_m,
                        BLOCK_N=block_n,
                        BLOCK_K=block_k,
                        num_stages=num_stages,
                        num_warps=num_warps,
                        matrix_instr_nonkdim=matrix_instr_nonkdim,
                        kpack=kpack,
                    )
        else:
            if (block_m, block_n, block_k, num_stages, num_warps, 0) not in used and (
                max_mm_configs is None or len(used) < max_mm_configs
            ):
                used.add((block_m, block_n, block_k, num_stages, num_warps, 0))
                yield triton_config(
                    BLOCK_M=block_m,
                    BLOCK_N=block_n,
                    BLOCK_K=block_k,
                    num_stages=num_stages,
                    num_warps=num_warps,
                )
