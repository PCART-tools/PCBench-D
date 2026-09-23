def use_triton_tma_template(*matrices: IRNode) -> bool:
    from torch.utils._triton import has_triton_stable_tma_api, has_triton_tma_device

    from .virtualized import V

    def _is_tma_compatible(x: IRNode) -> bool:
        if len(x.get_size()) != 2:
            return False

        dtype = x.get_dtype()
        if dtype not in (torch.float16, torch.bfloat16, torch.float8_e4m3fn):
            return False

        layout = x.get_layout()
        transposed = layout.is_transposed()
        if not (layout.is_contiguous() or transposed):
            return False

        inner_dim = layout.size[1]
        if transposed:
            inner_dim = layout.size[0]

        if dtype == torch.float8_e4m3fn and V.graph.sizevars.statically_known_lt(
            inner_dim, 32
        ):
            return False

        inner_bytes = inner_dim * dtype.itemsize
        return V.graph.sizevars.statically_known_multiple_of(inner_bytes, TMA_ALIGNMENT)

    if has_triton_stable_tma_api() and config.cpp_wrapper:
        # TODO(dberard) remove this when we get AOTI support for new TMA APIs (#155047)
        return False

    return (
        config.triton.enable_persistent_tma_matmul
        and has_triton_tma_device()
        and all(_is_tma_compatible(m) for m in matrices)
    )
