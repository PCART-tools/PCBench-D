@_onnx_symbolic("aten::mse_loss")
@symbolic_helper.parse_args("v", "v", "i")
def mse_loss(g: jit_utils.GraphContext, input, target, reduction):
    output = mul(g, sub(g, input, target), sub(g, input, target))
    if reduction == 0:
        return output
    elif reduction == 1:
        return g.op("ReduceMean", output, keepdims_i=0)
    elif reduction == 2:
        return symbolic_helper._reducesum_helper(g, output, keepdims_i=0)
    else:
        return symbolic_helper._onnx_unsupported(
            "mse_loss with reduction other than none, mean, or sum.", input
        )
