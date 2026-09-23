def is_integral(dtype: torch.dtype) -> bool:
    return dtype in (torch.bool, torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64)
