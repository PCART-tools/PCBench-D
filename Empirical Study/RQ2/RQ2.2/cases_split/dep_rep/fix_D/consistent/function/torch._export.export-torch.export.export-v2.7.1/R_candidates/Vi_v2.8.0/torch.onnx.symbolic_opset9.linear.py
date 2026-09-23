@_onnx_symbolic("aten::linear")
def linear(g: jit_utils.GraphContext, input, weight, bias):
    rank = symbolic_helper._get_tensor_rank(input)
    weight = t(g, weight)
    if rank == 2 and not bias.node().mustBeNone():
        alpha = g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))
        beta = g.op("Constant", value_t=torch.tensor(1, dtype=torch.int64))
        output = addmm(g, bias, input, weight, alpha, beta)
    else:
        output = matmul(g, input, weight)
        if not bias.node().mustBeNone():
            output = add(g, bias, output)

    return output
