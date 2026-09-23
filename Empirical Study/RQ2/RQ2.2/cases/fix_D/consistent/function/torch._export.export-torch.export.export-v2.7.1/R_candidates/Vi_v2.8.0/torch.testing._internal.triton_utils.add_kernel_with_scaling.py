    @triton.jit
    def add_kernel_with_scaling(
        in_ptr0,
        in_ptr1,
        out_ptr,
        n_elements,
        scaling_factor,
        BLOCK_SIZE: "tl.constexpr",
    ):
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        x = tl.load(in_ptr0 + offsets, mask=mask)
        y = tl.load(in_ptr1 + offsets, mask=mask)
        output = (x + y) * scaling_factor
        tl.store(out_ptr + offsets, output, mask=mask)
