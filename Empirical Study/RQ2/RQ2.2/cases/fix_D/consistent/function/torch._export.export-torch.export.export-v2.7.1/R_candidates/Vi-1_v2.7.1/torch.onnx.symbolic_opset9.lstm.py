@_onnx_symbolic("aten::lstm")
def lstm(g: jit_utils.GraphContext, *args):
    if symbolic_helper._is_tensor_list(args[3]):
        return _lstm_packed(g, *args)
    else:
        return _lstm_full(g, *args)
