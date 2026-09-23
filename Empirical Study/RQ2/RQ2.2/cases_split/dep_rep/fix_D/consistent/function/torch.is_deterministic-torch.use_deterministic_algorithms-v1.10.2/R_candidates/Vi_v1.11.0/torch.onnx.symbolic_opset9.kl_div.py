@parse_args("v", "v", "i", "b")
def kl_div(g, input, target, reduction, log_target):
    if log_target:
        output = _kl_div_log_target_impl(g, input, target)
    else:
        output = _kl_div_non_log_target_impl(g, input, target)

    if reduction == 0:
        return output
    elif reduction == 1:
        return g.op("ReduceMean", output, keepdims_i=0)
    elif reduction == 2:
        return sym_help._reducesum_helper(g, output, keepdims_i=0)
    else:
        return sym_help._onnx_unsupported("kl_div with reduction other than none, mean, or sum.")
