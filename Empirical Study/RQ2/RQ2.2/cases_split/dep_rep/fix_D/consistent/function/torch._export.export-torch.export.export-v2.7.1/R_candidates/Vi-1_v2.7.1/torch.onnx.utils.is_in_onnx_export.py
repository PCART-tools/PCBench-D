def is_in_onnx_export() -> bool:
    """Returns whether it is in the middle of ONNX export."""
    return GLOBALS.in_onnx_export
