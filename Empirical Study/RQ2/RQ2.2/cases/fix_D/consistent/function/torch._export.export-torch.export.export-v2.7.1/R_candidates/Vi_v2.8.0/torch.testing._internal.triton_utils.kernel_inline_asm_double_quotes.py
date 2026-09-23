    @triton.jit
    def kernel_inline_asm_double_quotes(
        in_ptr, out_ptr, numel, BLOCK_SIZE: tl.constexpr
    ):
        pid = tl.program_id(axis=0)
        offsets = tl.arange(0, BLOCK_SIZE) + pid * BLOCK_SIZE
        data = tl.load(in_ptr + offsets, mask=offsets < numel)
        cos_pow = tl.inline_asm_elementwise(
            asm="""
            {
                cos.approx.f32 $0, $1;
                ex2.approx.f32 $0, $0;
            }
                """,
            constraints=("=r, r"),
            args=[data],
            dtype=tl.float32,
            is_pure=True,
            pack=1,
        )
        tl.store(out_ptr + offsets, cos_pow, mask=offsets < numel)
