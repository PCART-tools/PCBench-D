def from_torch_dtype_to_onnx_dtype_str(dtype: torch.dtype | type) -> set[str]:
    return _TORCH_DTYPE_TO_COMPATIBLE_ONNX_TYPE_STRINGS[dtype]
