@_onnx_symbolic("aten::dropout_")
@_onnx_symbolic("aten::dropout")
@symbolic_helper.parse_args("v", "f", "i")
def dropout(g: jit_utils.GraphContext, input, p, train):
    symbolic_helper.check_training_mode(train, "dropout")
    # if train is False, dropout is no-op
    if not train:
        return input
    r, _ = g.op("Dropout", input, ratio_f=p, outputs=2)
    return r
