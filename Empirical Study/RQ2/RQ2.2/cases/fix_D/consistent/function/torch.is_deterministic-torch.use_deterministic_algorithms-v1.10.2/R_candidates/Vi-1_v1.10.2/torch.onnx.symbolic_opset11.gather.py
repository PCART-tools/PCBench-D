@parse_args("v", "i", "v", "v")
def gather(g, self, dim, index, sparse_grad=False):
    if sym_help._maybe_get_const(sparse_grad, "i"):
        return _unimplemented("gather", "sparse_grad == True")
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", self, dim, index, sparse_grad, operator_s="gather")
    return g.op("GatherElements", self, index, axis_i=dim)
