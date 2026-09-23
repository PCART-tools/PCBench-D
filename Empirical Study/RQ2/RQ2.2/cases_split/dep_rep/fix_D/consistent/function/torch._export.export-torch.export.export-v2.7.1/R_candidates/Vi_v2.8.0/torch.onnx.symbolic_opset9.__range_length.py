@_onnx_symbolic("aten::__range_length")
# Source code for aten op can be found here: pytorch/torch/csrc/jit/runtime/register_prim_ops.cpp
# if (step > 0 && lo < hi) {
#   push(stack, 1 + (hi - 1 - lo) / step);
# } else if (step < 0 && lo > hi) {
#   push(stack, 1 + (lo - 1 - hi) / (0 - step));
# } else {
#  push(stack, 0);
# }
def __range_length(g: jit_utils.GraphContext, lo, hi, step):
    sub = g.op("Sub", hi, lo)
    div = g.op("Ceil", true_divide(g, sub, step))
    return g.op("Cast", div, to_i=_C_onnx.TensorProtoDataType.INT64)
