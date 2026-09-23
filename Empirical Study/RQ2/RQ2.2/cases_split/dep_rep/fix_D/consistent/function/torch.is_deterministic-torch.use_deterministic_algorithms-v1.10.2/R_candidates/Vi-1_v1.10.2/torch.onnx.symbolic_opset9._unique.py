@parse_args("v", "i", "i")
def _unique(g, input, sorted, return_inverse):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, operator_s="_unique", sorted_i=sorted,
                    return_inverse_i=return_inverse, outputs=2)
    else:
        return sym_help._onnx_unsupported("_unique")
