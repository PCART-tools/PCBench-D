@_onnx_symbolic("aten::gather")
@symbolic_helper.parse_args("v", "i", "v", "v")
def gather(g: jit_utils.GraphContext, self, dim, index, sparse_grad=False):
    if symbolic_helper._maybe_get_const(sparse_grad, "i"):
        return symbolic_helper._unimplemented("gather", "sparse_grad == True", self)
    # NOTE: This workaround is needed since GatherElement is only supported
    #       since opset 11, and Gather in ONNX is not the same as torch.gather.
    scalar_type = _type_utils.JitScalarType.from_value(self)
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    depth = size(g, self, g.op("Constant", value_t=torch.LongTensor([dim])))
    index = g.op(
        "Cast",
        g.op("OneHot", index, depth, values, axis_i=dim),
        to_i=scalar_type.onnx_type(),
    )
    mul = g.op("Mul", symbolic_helper._unsqueeze_helper(g, self, [dim + 1]), index)
    return symbolic_helper._reducesum_helper(g, mul, axes_i=[dim], keepdims_i=0)
