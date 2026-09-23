def type_as(g, self, other):
    self_dtype = sym_help._try_get_scalar_type(self)
    other_dtype = sym_help._try_get_scalar_type(other)
    if self_dtype == other_dtype and self_dtype is not None:
        return self
    if other_dtype is not None:
        return g.op("Cast", self, to_i=sym_help.cast_pytorch_to_onnx[other_dtype])
    else:
        if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
            # We don't know the type of other, bail by emitting ATen
            return g.op("ATen", self, other, operator_s="type_as")
        else:
            raise RuntimeError("Unsupported: ONNX export of type_as for tensor "
                               "of unknown dtype. Please check if the dtype of the "
                               "parameter passed to the type_as function is correct.")
