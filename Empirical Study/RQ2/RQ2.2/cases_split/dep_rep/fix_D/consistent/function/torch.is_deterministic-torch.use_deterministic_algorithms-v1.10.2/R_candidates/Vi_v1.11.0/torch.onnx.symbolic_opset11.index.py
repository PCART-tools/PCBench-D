def index(g, self, index):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", self, index, operator_s="index")

    if sym_help._is_packed_list(index):
        indices = sym_help._unpack_list(index)
    else:
        indices = [index]

    # Handle single mask index.
    if len(indices) == 1:
        index = indices[0]
        if not sym_help._is_none(index) and (index.type().scalarType() == "Bool" or index.type().scalarType() == "Byte"):
            from torch.onnx.symbolic_opset9 import nonzero
            index = nonzero(g, index)
            return g.op("GatherND", self, index)
    from torch.onnx.symbolic_opset9 import index as index_opset9
    return index_opset9(g, self, index)
