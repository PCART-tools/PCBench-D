def _is_amx_fp16_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AMX FP16."""
    return torch._C._cpu._is_amx_fp16_supported()
