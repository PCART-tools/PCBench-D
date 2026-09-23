    @triton.jit
    def inline_asm_kernel_is_pure_false(
        X, Y, Z, n: "tl.constexpr", BLOCK: "tl.constexpr"
    ):
        x = tl.load(X + tl.arange(0, BLOCK))
        y = tl.load(Y + tl.arange(0, BLOCK))
        s = tl.full([BLOCK], n, tl.int32)
        z = tl.inline_asm_elementwise(
            "shf.l.wrap.b32 $0, $1, $2, $3;",
            "=r,r, r, r",
            [x, y, s],
            dtype=tl.int32,
            is_pure=False,
            pack=1,
        )
        tl.store(Z + tl.arange(0, BLOCK), z)
