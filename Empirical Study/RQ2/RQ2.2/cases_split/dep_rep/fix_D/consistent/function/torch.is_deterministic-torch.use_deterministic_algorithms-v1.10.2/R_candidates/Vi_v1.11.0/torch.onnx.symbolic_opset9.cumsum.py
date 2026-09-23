@parse_args("v", "i", "none")
def cumsum(g, input, dim, dtype):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        if dtype.node().kind() != "prim::Constant":
            return _unimplemented(name, "dtype")
        return g.op("ATen", input, operator_s="cumsum", dim_i=dim)
    else:
        sym_help._onnx_opset_unsupported("cumsum", 9, 11)
