@_onnx_symbolic("aten::index_copy")
def index_copy(g: jit_utils.GraphContext, self, dim, index, source):
    _expanded_index_shape, expanded_index = symbolic_helper._index_fill_reshape_helper(
        g, self, dim, index
    )
    return scatter(g, self, dim, expanded_index, source)
