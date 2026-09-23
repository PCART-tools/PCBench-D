    @triton.jit
    def add_kernel_with_tma_2d(
        in_desc_ptr0,
        in_desc_ptr1,
        out_desc_ptr,
        BLOCK_SIZE_X: "tl.constexpr",
        BLOCK_SIZE_Y: "tl.constexpr",
    ):
        pid_x = tl.program_id(axis=0)
        pid_y = tl.program_id(axis=1)
        offset_x = pid_x * BLOCK_SIZE_X
        offset_y = pid_y * BLOCK_SIZE_Y

        x = tl._experimental_descriptor_load(
            in_desc_ptr0,
            [offset_x, offset_y],
            [BLOCK_SIZE_X, BLOCK_SIZE_Y],
            tl.float32,
        )
        y = tl._experimental_descriptor_load(
            in_desc_ptr1,
            [offset_x, offset_y],
            [BLOCK_SIZE_X, BLOCK_SIZE_Y],
            tl.float32,
        )

        output = x + y

        tl._experimental_descriptor_store(
            out_desc_ptr,
            output,
            [offset_x, offset_y],
        )
