@parse_args("v", "i", "v", "v")
def scatter(g, self, dim, index, src):
    from torch.onnx.symbolic_opset9 import expand_as
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", self, dim, index, src, operator_s="scatter")
    src_type = src.type().scalarType()
    src = sym_help._maybe_get_scalar(src)
    if sym_help._is_value(src):
        return g.op("ScatterElements", self, index, src, axis_i=dim)
    else:
        # Check if scalar "src" has same type as self (PyTorch allows different
        # type for scalar src (but not when src is tensor)). If not, insert Cast node.
        if self.type().scalarType() != src_type:
            src = g.op("Cast", src, to_i=sym_help.cast_pytorch_to_onnx[self.type().scalarType()])
        return g.op("ScatterElements", self, index, expand_as(g, src, index), axis_i=dim)
