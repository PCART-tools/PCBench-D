def one_hot(g, self, num_classes):
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    # onnxruntime supports limited type combinations for OneHot.
    if num_classes.type().scalarType() in ("Byte", "Char", "Int", "Short"):
        num_classes = g.op("Cast", num_classes, to_i=sym_help.cast_pytorch_to_onnx["Long"])
    return g.op("OneHot", self, num_classes, values, axis_i=-1)
