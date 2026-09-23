    @triton.jit
    def add_kernel_on_device_tma_old_api(
        a_ptr,
        b_ptr,
        c_ptr,
        m,
        n,
        workspace,
        BLOCK_SIZE: "tl.constexpr",
    ):
        a_desc_ptr = workspace
        b_desc_ptr = workspace + 128
        c_desc_ptr = workspace + 256
        tl.extra.cuda.experimental_device_tensormap_create2d(
            desc_ptr=a_desc_ptr,
            global_address=a_ptr,
            load_size=[BLOCK_SIZE, BLOCK_SIZE],
            global_size=[m, n],
            element_ty=a_ptr.dtype.element_ty,
        )
        tl.extra.cuda.experimental_device_tensormap_create2d(
            desc_ptr=b_desc_ptr,
            global_address=b_ptr,
            load_size=[BLOCK_SIZE, BLOCK_SIZE],
            global_size=[m, n],
            element_ty=b_ptr.dtype.element_ty,
        )
        tl.extra.cuda.experimental_device_tensormap_create2d(
            desc_ptr=c_desc_ptr,
            global_address=c_ptr,
            load_size=[BLOCK_SIZE, BLOCK_SIZE],
            global_size=[m, n],
            element_ty=c_ptr.dtype.element_ty,
        )

        tl.extra.cuda.experimental_tensormap_fenceproxy_acquire(a_desc_ptr)
        tl.extra.cuda.experimental_tensormap_fenceproxy_acquire(b_desc_ptr)
        tl.extra.cuda.experimental_tensormap_fenceproxy_acquire(c_desc_ptr)

        pid_x = tl.program_id(axis=0)
        pid_y = tl.program_id(axis=1)
        offset_x = pid_x * BLOCK_SIZE
        offset_y = pid_y * BLOCK_SIZE

        # Load data using the tensor descriptors
        a = tl._experimental_descriptor_load(
            a_desc_ptr,
            [offset_x, offset_y],
            [BLOCK_SIZE, BLOCK_SIZE],
            tl.float32,
        )
        b = tl._experimental_descriptor_load(
            b_desc_ptr,
            [offset_x, offset_y],
            [BLOCK_SIZE, BLOCK_SIZE],
            tl.float32,
        )

        # Perform addition
        output = a + b

        # Store the result
        tl._experimental_descriptor_store(
            c_desc_ptr,
            output,
            [offset_x, offset_y],
        )
