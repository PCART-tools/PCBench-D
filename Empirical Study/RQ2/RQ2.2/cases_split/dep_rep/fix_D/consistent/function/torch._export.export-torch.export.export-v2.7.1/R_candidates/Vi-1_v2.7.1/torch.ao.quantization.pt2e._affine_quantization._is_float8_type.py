def _is_float8_type(dtype: torch.dtype) -> bool:
    fp8_types = {
        torch.float8_e4m3fn,
        torch.float8_e4m3fnuz,
        torch.float8_e5m2,
        torch.float8_e5m2fnuz,
    }
    return dtype in fp8_types
