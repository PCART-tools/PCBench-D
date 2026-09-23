def tma_options() -> dict[str, Any]:
    from torch.utils._triton import has_triton_stable_tma_api

    return {"TMA_EXPERIMENTAL_API": not has_triton_stable_tma_api()}
