@_onnx_symbolic("aten::index_put")
def index_put(g: jit_utils.GraphContext, self, indices_list_value, values, accumulate):
    if symbolic_helper._is_packed_list(indices_list_value):
        indices_list = symbolic_helper._unpack_list(indices_list_value)
    else:
        indices_list = [indices_list_value]

    accumulate = symbolic_helper._parse_arg(accumulate, "b")

    if len(indices_list) == 0:
        if accumulate:
            return add(g, self, values)
        return values
    symbolic_helper._onnx_opset_unsupported("index_put", 9, 11, self)
