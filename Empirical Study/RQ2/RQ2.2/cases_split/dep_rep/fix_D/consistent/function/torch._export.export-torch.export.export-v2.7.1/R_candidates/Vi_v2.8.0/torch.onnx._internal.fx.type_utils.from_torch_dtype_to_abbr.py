def from_torch_dtype_to_abbr(dtype: torch.dtype | None) -> str:
    if dtype is None:
        return ""
    return _TORCH_DTYPE_TO_ABBREVIATION.get(dtype, "")
