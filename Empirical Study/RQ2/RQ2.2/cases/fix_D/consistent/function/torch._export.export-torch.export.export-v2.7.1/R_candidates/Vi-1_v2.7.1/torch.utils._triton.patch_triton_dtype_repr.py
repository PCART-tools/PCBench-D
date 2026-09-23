def patch_triton_dtype_repr():
    import triton

    # Hack to get triton dtype repr to produce an evaluatable expression
    # triton.language.float32 emits triton.language.fp32 which does not
    # exist
    # REMOVE when https://github.com/openai/triton/pull/3342 lands
    triton.language.dtype.__repr__ = lambda self: dtype_to_string(self)
