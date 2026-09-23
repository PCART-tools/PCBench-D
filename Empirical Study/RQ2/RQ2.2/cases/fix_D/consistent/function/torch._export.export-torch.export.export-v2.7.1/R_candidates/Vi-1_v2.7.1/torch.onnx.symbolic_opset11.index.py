@_onnx_symbolic("aten::index")
def index(g: jit_utils.GraphContext, self, index):
    if symbolic_helper._is_packed_list(index):
        indices = symbolic_helper._unpack_list(index)
    else:
        indices = [index]

    # Handle single mask index.
    if len(indices) == 1:
        index = indices[0]
        if not symbolic_helper._is_none(index) and (
            symbolic_helper._is_bool(index)
            or _type_utils.JitScalarType.from_value(index)
            == _type_utils.JitScalarType.UINT8
        ):
            index = opset9.nonzero(g, index)
            return g.op("GatherND", self, index)
    return opset9.index(g, self, index)
