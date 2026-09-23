@parse_args("v", "i", "i", "i")
def _unique2(g, input, sorted, return_inverse, return_counts):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, operator_s="_unique2", sorted_i=sorted,
                    return_inverse_i=return_inverse, return_counts_i=return_counts,
                    outputs=3)
    else:
        sym_help._onnx_opset_unsupported("_unique2", 9, 11)
