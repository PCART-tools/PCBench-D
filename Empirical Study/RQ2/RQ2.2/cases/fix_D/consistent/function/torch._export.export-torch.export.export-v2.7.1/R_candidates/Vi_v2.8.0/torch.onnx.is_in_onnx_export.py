def is_in_onnx_export() -> bool:
    """Returns whether it is in the middle of ONNX export."""
    from torch.onnx._globals import GLOBALS
    from torch.onnx._internal.exporter import _flags

    return GLOBALS.in_onnx_export or _flags._is_onnx_exporting
