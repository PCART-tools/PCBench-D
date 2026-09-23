@parse_args("v", "v", "i", "f")
def cosine_similarity(g, x1, x2, dim, eps):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", x1, x2, dim_i=dim, eps_f=eps, operator_s="cosine_similarity")
    else:
        return sym_help._onnx_unsupported("cosine_similarity")
