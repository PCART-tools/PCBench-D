    @triton.jit
    def add_kernel_with_tma_1d_new_api(
        in_desc_ptr0,
        in_desc_ptr1,
        out_desc_ptr,
        BLOCK_SIZE: "tl.constexpr",
    ):
        pid = tl.program_id(axis=0)
        offset = pid * BLOCK_SIZE

        a = tl.load_tensor_descriptor(
            in_desc_ptr0,
            [offset],
        )
        b = tl.load_tensor_descriptor(
            in_desc_ptr1,
            [offset],
        )

        output = a + b

        tl.store_tensor_descriptor(
            out_desc_ptr,
            [offset],
            output,
        )
