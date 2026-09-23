def _slice_helper(g, input, axes, starts, ends, steps=None, dynamic_slice=False):
    if _export_onnx_opset_version <= 9:
        from torch.onnx.symbolic_opset9 import _slice as _slice9
        return _slice9(g, input, axes, starts, ends)
    else:
        from torch.onnx.symbolic_opset10 import _slice as _slice10
        return _slice10(g, input, axes, starts, ends, steps, dynamic_slice)
