@functools.lru_cache(None)
def init_gpu_context(device: torch.device) -> None:
    # Backward will error with cuda Fake Tensors if no cuda tensors have been initialized first
    if torch.cuda.is_available() or torch.xpu.is_available():
        (
            torch.empty(1, device=device)
            if torch.version.hip is None
            else torch.zeros(1, device=device)
        )
