    @triton.jit
    def kernel_with_docstring_double_quotes(out_ptr, numel, BLOCK_SIZE: tl.constexpr):
        """
        This kernel contains a triple-quote docstring w/ double quotes.
        Make sure that codegen sanitizes the docstring.
        """
        pid = tl.program_id(axis=0)
        offsets = tl.arange(0, BLOCK_SIZE) + pid * BLOCK_SIZE
        ones = tl.full([BLOCK_SIZE], 1.0, dtype=tl.float32)
        tl.store(out_ptr + offsets, ones, mask=offsets < numel)
