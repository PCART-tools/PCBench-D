def is_gpu(device: Optional[str]) -> bool:
    return device in GPU_TYPES
