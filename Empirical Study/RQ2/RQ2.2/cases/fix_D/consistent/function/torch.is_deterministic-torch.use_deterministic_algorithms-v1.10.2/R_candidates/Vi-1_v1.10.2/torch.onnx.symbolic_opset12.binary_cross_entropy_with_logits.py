@parse_args("v", "v", "v", "v", "i")
def binary_cross_entropy_with_logits(g, input, target, weight, pos_weight, reduction):
    from torch.onnx.symbolic_opset9 import sigmoid, log, sub, neg, mul, add
    p = g.op("Constant", value_t=torch.tensor([1]))
    sig_x = sigmoid(g, input)
    log_sig_x = log(g, sig_x)
    sub_1_x = sub(g, p, sig_x)
    sub_1_y = sub(g, p, target)
    log_1_x = log(g, sub_1_x)
    if pos_weight is None or sym_help._is_none(pos_weight):
        output = neg(g, add(g, mul(g, target, log_sig_x), mul(g, sub_1_y, log_1_x)))
    else:
        output = neg(g, add(g, mul(g, mul(g, target, log_sig_x), pos_weight), mul(g, sub_1_y, log_1_x)))

    if weight is not None and not sym_help._is_none(weight):
        output = mul(g, weight, output)

    reduction = sym_help._maybe_get_const(reduction, "i")
    if reduction == 0:
        return output
    elif reduction == 1:
        return g.op("ReduceMean", output)
    elif reduction == 2:
        return g.op("ReduceSum", output)
    else:
        return sym_help._onnx_unsupported("binary_cross_entropy_with_logits with reduction other than none, mean, or sum")
