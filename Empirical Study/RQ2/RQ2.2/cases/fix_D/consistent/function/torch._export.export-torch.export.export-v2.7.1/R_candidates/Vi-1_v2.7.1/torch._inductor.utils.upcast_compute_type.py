def upcast_compute_type(dtype: torch.dtype) -> torch.dtype:
    """Maybe upcast [b]float16 to float32"""
    if config.triton.codegen_upcast_to_fp32 and (
        dtype in (torch.float16, torch.bfloat16)
    ):
        return torch.float32
    return dtype
