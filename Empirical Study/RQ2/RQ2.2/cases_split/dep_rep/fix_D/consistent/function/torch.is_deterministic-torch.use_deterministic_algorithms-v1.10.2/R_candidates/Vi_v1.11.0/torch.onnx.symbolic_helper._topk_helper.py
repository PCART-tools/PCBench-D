def _topk_helper(g, input, k, dim, largest=True, sorted=False, out=None):
    if out is not None:
        _unimplemented("TopK", "Out parameter is not supported")
    if not _is_value(k):
        k = g.op("Constant", value_t=torch.tensor([k], dtype=torch.int64))
    else:
        k = _reshape_helper(g, k, g.op("Constant", value_t=torch.tensor([1])))
    if _export_onnx_opset_version <= 10:
        if not largest:
            _unimplemented("TopK", "Ascending is not supported")
        return g.op("TopK", input, k, axis_i=dim, outputs=2)
    else:
        return g.op("TopK", input, k, axis_i=dim, largest_i=largest, sorted_i=sorted, outputs=2)
