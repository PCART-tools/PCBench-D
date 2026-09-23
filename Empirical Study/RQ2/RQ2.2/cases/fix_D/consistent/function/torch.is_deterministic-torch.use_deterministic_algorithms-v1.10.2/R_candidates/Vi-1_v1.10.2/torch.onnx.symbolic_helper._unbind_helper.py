def _unbind_helper(g, self, dim, _outputs):
    if _export_onnx_opset_version < 11:
        from torch.onnx.symbolic_opset9 import unbind
    elif _export_onnx_opset_version <= 12:
        from torch.onnx.symbolic_opset11 import unbind  # type: ignore[no-redef]
    else:
        from torch.onnx.symbolic_opset13 import unbind  # type: ignore[no-redef]
    return unbind(g, self, dim, _outputs)
