def __range_length(g, lo, hi, step):
    sub = g.op("Sub", hi, lo)
    div = g.op("Ceil", true_divide(g, sub, step))
    return g.op("Cast", div, to_i=sym_help.cast_pytorch_to_onnx["Long"])
