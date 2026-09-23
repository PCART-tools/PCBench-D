    @triton.jit
    def add_4_times_kernel(
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
        for i in range(2):
            output = x + y
            tl.store(out_ptr + offsets, output, mask=mask)
        i = 2
        while i > 0:
            i -= 1
            output = x + y
            tl.store(out_ptr + offsets, output, mask=mask)
