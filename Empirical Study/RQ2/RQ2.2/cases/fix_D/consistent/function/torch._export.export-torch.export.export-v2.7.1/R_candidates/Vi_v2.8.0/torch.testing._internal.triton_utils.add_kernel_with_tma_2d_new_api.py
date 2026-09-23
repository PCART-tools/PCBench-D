    @triton.jit
    def add_kernel_with_tma_2d_new_api(
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

        x = tl.load_tensor_descriptor(
            in_desc_ptr0,
            [offset_x, offset_y],
        )
        y = tl.load_tensor_descriptor(
            in_desc_ptr1,
            [offset_x, offset_y],
        )

        output = x + y

        tl.store_tensor_descriptor(
            out_desc_ptr,
            [offset_x, offset_y],
            output,
        )
