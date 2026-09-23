@_onnx_symbolic("aten::stack")
@symbolic_helper.parse_args("v", "i")
def stack(g: jit_utils.GraphContext, tensor_list, dim):
    unsqueezed = [
        symbolic_helper._unsqueeze_helper(g, t, [dim])
        for t in symbolic_helper._unpack_list(tensor_list)
    ]
    return g.op("Concat", *unsqueezed, axis_i=dim)
