    @triton.autotune(
        configs=[
            triton.Config({"BLOCK_SIZE": 16}, num_stages=2, num_warps=2),
        ],
        key=[],
    )
    @triton.jit
    def add_kernel_autotuned_weird_param_order(
        in_ptr0,
        in_ptr1,
        n_elements,
        BLOCK_SIZE: "tl.constexpr",
        out_ptr,
    ):
        # out_ptr is after an autotuned param that's declared as tl.constexpr.
        # This param ordering can create bugs if not handled correctly.
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        x = tl.load(in_ptr0 + offsets, mask=mask)
        y = tl.load(in_ptr1 + offsets, mask=mask)
        output = x + y
        tl.store(out_ptr + offsets, output, mask=mask)
