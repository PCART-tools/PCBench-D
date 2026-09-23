def is_optional_onnx_dtype_str(onnx_type_str: str) -> bool:
    return onnx_type_str in _OPTIONAL_ONNX_DTYPE_STR
