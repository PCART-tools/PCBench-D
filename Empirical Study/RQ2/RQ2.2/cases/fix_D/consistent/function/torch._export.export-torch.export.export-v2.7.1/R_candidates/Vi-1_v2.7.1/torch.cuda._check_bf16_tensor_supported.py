@lru_cache(maxsize=16)
def _check_bf16_tensor_supported(device: _device_t):
    try:
        torch.tensor([1.0], dtype=torch.bfloat16, device=device)
        return True
    except Exception:
        return False
