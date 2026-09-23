def device_need_guard(device: str) -> bool:
    return is_gpu(device)
