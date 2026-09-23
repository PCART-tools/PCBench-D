    @triton.autotune(
        configs=[
            triton.Config({"BLOCK_SIZE": 128}, num_stages=3, num_warps=8),
            triton.Config({"BLOCK_SIZE": 64}, num_stages=4, num_warps=4),
        ],
        key=[],
        warmup=10,
        rep=20,
        prune_configs_by={"early_config_prune": _dummy_early_config_prune},
    )
    @triton.jit
    def add_kernel_autotuned_with_unsupported_args(
        in_ptr0,
        in_ptr1,
        out_ptr,
        n_elements,
        BLOCK_SIZE: "tl.constexpr",
    ):
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        x = tl.load(in_ptr0 + offsets, mask=mask)
        y = tl.load(in_ptr1 + offsets, mask=mask)
        output = x + y
        tl.store(out_ptr + offsets, output, mask=mask)
