    @triton.jit
    def kernel_with_block_ptr_2d(
        x_ptr,
        output_ptr,
        n_elements,
        BLOCK_SIZE: tl.constexpr,
    ):
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        x = tl.load(
            tl.make_block_ptr(
                base=x_ptr,
                shape=[n_elements, 1],
                strides=[1, 1],
                offsets=[block_start, 0],
                block_shape=[BLOCK_SIZE, 1],
                order=[1, 0],
            ),
            boundary_check=[0],
        )
        output = x
        tl.store(
            tl.make_block_ptr(
                base=output_ptr,
                shape=[n_elements, 1],
                strides=[1, 1],
                offsets=[block_start, 0],
                block_shape=[BLOCK_SIZE, 1],
                order=[1, 0],
            ),
            output,
            boundary_check=[0],
        )
