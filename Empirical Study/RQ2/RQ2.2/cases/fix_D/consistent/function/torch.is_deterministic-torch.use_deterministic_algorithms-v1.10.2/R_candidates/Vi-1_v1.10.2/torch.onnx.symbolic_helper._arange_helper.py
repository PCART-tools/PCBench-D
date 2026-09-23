def _arange_helper(g, *args):
    if _export_onnx_opset_version <= 10:
        from torch.onnx.symbolic_opset9 import arange
    else:
        from torch.onnx.symbolic_opset11 import arange  # type: ignore[no-redef]
    return arange(g, *args)
