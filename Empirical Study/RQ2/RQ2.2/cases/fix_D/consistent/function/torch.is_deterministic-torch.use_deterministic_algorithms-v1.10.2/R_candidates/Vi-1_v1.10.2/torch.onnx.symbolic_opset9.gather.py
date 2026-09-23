@parse_args("v", "i", "v", "v")
def gather(g, self, dim, index, sparse_grad=False):
    if sym_help._maybe_get_const(sparse_grad, "i"):
        return _unimplemented("gather", "sparse_grad == True")
    # NOTE: This workaround is needed since GatherElement is only supported
    #       since opset 11, and Gather in ONNX is not the same as torch.gather.
    dtype = self.type().scalarType()
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    depth = size(g, self, g.op("Constant", value_t=torch.LongTensor([dim])))
    index = g.op("Cast", g.op("OneHot", index, depth, values, axis_i=dim), to_i=sym_help.cast_pytorch_to_onnx[dtype])
    mul = g.op("Mul", sym_help._unsqueeze_helper(g, self, [dim + 1]), index)
    return sym_help._reducesum_helper(g, mul, axes_i=[dim], keepdims_i=0)
