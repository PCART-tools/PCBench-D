    @triton.jit
    def add_kernel_with_none_param_and_equal_to_1_arg(
        in_ptr0,
        in_ptr1,  # in_ptr1 could be None
        out_ptr,
        n_elements,
        stride,
        ARGS_PASSED: "tl.constexpr",
        BLOCK_SIZE: "tl.constexpr",
    ):
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        x = tl.load(in_ptr0 + offsets * stride, mask=mask)
        if ARGS_PASSED == "two":
            y = tl.load(in_ptr1 + offsets, mask=mask)
            output = x + y
        else:
            output = x
        tl.store(out_ptr + offsets * stride, output, mask=mask)
