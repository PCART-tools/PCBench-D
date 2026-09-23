def _squeeze_helper(g, input, axes_i):
    if _export_onnx_opset_version >= 13:
        axes = g.op("Constant", value_t=torch.tensor(axes_i, dtype=torch.long))
        return g.op("Squeeze", input, axes)
    else:
        return g.op("Squeeze", input, axes_i=axes_i)
