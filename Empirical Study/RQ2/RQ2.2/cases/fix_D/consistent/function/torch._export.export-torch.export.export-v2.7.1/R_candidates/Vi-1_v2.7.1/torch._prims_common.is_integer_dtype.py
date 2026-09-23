def is_integer_dtype(dtype: torch.dtype) -> bool:
    assert isinstance(dtype, torch.dtype)
    return dtype in _integer_dtypes
