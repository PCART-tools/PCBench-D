    @triton.jit
    def add_kernel_with_tma_1d_old_api(
        in_desc_ptr0,
        in_desc_ptr1,
        out_desc_ptr,
        BLOCK_SIZE: "tl.constexpr",
    ):
        pid = tl.program_id(axis=0)
        offset = pid * BLOCK_SIZE

        a = tl._experimental_descriptor_load(
            in_desc_ptr0,
            [offset],
            [BLOCK_SIZE],
            tl.float32,
        )
        b = tl._experimental_descriptor_load(
            in_desc_ptr1,
            [offset],
            [BLOCK_SIZE],
            tl.float32,
        )

        output = a + b

        tl._experimental_descriptor_store(
            out_desc_ptr,
            output,
            [offset],
        )
