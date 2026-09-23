def _sort_helper(g, input, dim, decending=True, out=None):
    if out is not None:
        _unimplemented("Sort", "Out parameter is not supported")
    shape_ = g.op("Shape", input)
    dim_size_ = g.op("Gather", shape_, g.op("Constant", value_t=torch.tensor([dim], dtype=torch.int64)))
    if _export_onnx_opset_version <= 10:
        if not decending:
            _unimplemented("Sort", "Ascending is not supported")
        return g.op("TopK", input, dim_size_, axis_i=dim, outputs=2)
    else:
        return g.op("TopK", input, dim_size_, axis_i=dim, largest_i=decending, outputs=2)
