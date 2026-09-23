    @triton.jit
    def add_kernel_on_device_tma_new_api(
        a_ptr,
        b_ptr,
        c_ptr,
        m,
        n,
        workspace,  # unused but left here to match the old API kernel
        BLOCK_SIZE: "tl.constexpr",
    ):
        # Create tensor descriptors using the new API
        a_desc = tl.make_tensor_descriptor(
            base=a_ptr,
            shape=[m, n],
            strides=[n, 1],
            block_shape=[BLOCK_SIZE, BLOCK_SIZE],
        )
        b_desc = tl.make_tensor_descriptor(
            base=b_ptr,
            shape=[m, n],
            strides=[n, 1],
            block_shape=[BLOCK_SIZE, BLOCK_SIZE],
        )
        c_desc = tl.make_tensor_descriptor(
            base=c_ptr,
            shape=[m, n],
            strides=[n, 1],
            block_shape=[BLOCK_SIZE, BLOCK_SIZE],
        )

        pid_x = tl.program_id(axis=0)
        pid_y = tl.program_id(axis=1)
        offset_x = pid_x * BLOCK_SIZE
        offset_y = pid_y * BLOCK_SIZE

        # Load data using the tensor descriptors with the new API
        a = tl.load_tensor_descriptor(
            a_desc,
            [offset_x, offset_y],
        )
        b = tl.load_tensor_descriptor(
            b_desc,
            [offset_x, offset_y],
        )

        # Perform addition
        output = a + b

        # Store the result with the new API
        tl.store_tensor_descriptor(
            c_desc,
            [offset_x, offset_y],
            output,
        )
