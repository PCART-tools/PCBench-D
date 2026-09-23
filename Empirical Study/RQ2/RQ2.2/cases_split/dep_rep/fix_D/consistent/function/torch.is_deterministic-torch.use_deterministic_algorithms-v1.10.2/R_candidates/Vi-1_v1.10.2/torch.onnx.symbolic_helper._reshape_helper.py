def _reshape_helper(g, input, shape, allowzero=0):
    shape = _maybe_get_const(shape, "is")
    if not _is_value(shape):
        shape = g.op("Constant", value_t=torch.LongTensor(shape))
    if _export_onnx_opset_version <= 13:
        return g.op("Reshape", input, shape)
    else:
        warnings.warn("allowzero=0 by default. In order to honor zero value in shape use allowzero=1")
        return g.op("Reshape", input, shape, allowzero_i=allowzero)
