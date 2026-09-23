def _lt_helper(g, input, other):
    if _export_onnx_opset_version <= 8:
        from torch.onnx.symbolic_opset8 import lt as _lt8
        return _lt8(g, input, other)
    else:
        from torch.onnx.symbolic_opset9 import lt as _lt9
        return _lt9(g, input, other)
