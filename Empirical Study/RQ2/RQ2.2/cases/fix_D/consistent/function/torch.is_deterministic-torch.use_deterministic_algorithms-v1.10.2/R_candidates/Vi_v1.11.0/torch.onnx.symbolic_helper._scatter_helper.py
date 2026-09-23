def _scatter_helper(g, self, dim, index, src):
    if _export_onnx_opset_version <= 10:
        from torch.onnx.symbolic_opset9 import scatter
    else:
        # for mypy, scatter was imported two lines above
        from torch.onnx.symbolic_opset11 import scatter  # type: ignore[no-redef]
    return scatter(g, self, dim, index, src)
