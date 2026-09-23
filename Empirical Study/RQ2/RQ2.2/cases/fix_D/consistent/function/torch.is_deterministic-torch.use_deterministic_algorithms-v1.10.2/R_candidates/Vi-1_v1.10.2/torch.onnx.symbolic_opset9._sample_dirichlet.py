def _sample_dirichlet(g, self, generator):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        if not sym_help._is_none(generator):
            return _unimplemented("_sample_dirichlet",
                                  "We are not able to export generator")
        return g.op("ATen", self, operator_s="_sample_dirichlet")
    else:
        return sym_help._onnx_unsupported("_sample_dirichlet")
