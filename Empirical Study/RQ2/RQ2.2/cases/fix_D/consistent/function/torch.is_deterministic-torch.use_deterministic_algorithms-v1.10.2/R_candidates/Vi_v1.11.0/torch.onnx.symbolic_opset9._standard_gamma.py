def _standard_gamma(g, self, generator):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        if not sym_help._is_none(generator):
            return _unimplemented("_standard_gamma",
                                  "We are not able to export generator")
        return g.op("ATen", self, operator_s="_standard_gamma")
    else:
        return sym_help._onnx_unsupported("_standard_gamma")
