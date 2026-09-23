@_onnx_symbolic("aten::kl_div")
@symbolic_helper.parse_args("v", "v", "i", "b")
def kl_div(g: jit_utils.GraphContext, input, target, reduction, log_target):
    if log_target:
        output = _kl_div_log_target_impl(g, input, target)
    else:
        output = _kl_div_non_log_target_impl(g, input, target)

    if reduction == 0:
        return output
    elif reduction == 1:
        return g.op("ReduceMean", output, keepdims_i=0)
    elif reduction == 2:
        return symbolic_helper._reducesum_helper(g, output, keepdims_i=0)
    else:
        return symbolic_helper._onnx_unsupported(
            "kl_div with reduction other than none, mean, or sum.", input
        )
