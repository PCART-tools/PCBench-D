    @triton.jit
    def add_kernel_with_import(
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
        x = load(in_ptr0 + offsets, mask=mask)
        y = load(in_ptr1 + offsets, mask=mask)
        output = x + y
        store(out_ptr + offsets, output, mask=mask)
