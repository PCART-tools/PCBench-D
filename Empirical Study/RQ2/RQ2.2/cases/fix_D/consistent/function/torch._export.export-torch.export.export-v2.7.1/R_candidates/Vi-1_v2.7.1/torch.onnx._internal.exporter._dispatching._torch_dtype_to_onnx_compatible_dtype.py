def _torch_dtype_to_onnx_compatible_dtype(dtype: torch.dtype) -> ir.DataType:
    return _TORCH_DTYPE_TO_ONNX_COMPATIBLE[dtype]
