@_onnx_symbolic("aten::as_strided")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "v", "is", "i")
def as_strided(g: jit_utils.GraphContext, self, sizes, strides, offset=None):
    sizes = symbolic_helper._maybe_get_const(sizes, "is")
    rank = len(strides)
    self_1d = symbolic_helper._reshape_helper(
        g, self, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64))
    )
    ind: torch.Tensor | None
    if not symbolic_helper._is_value(sizes):
        ind = torch.tensor([0], dtype=torch.long)
        for i, (size, stride) in enumerate(zip(sizes, strides)):
            r_size = [1] * rank
            r_size[i] = -1
            ind = ind + torch.arange(size).view(r_size) * stride
        if offset:
            ind = ind + offset
        return g.op("Gather", self_1d, g.op("Constant", value_t=ind))
    else:
        ind = None
        for i, stride in enumerate(strides):
            r_size = [1] * rank
            r_size[i] = -1
            size = select(
                g,
                sizes,
                g.op("Constant", value_t=torch.tensor([0])),
                g.op("Constant", value_t=torch.tensor(i)),
            )
            tmp_ind = symbolic_helper._reshape_helper(
                g,
                arange(g, size, 4, None, None, None),
                g.op("Constant", value_t=torch.tensor(r_size)),
            )
            tmp_ind = g.op(
                "Mul", tmp_ind, g.op("Constant", value_t=torch.tensor([stride]))
            )
            if ind is None:
                ind = tmp_ind
            else:
                ind = g.op("Add", ind, tmp_ind)
        if offset:
            ind = g.op("Add", ind, g.op("Constant", torch.tensor([offset])))
        return g.op("Gather", self_1d, ind)
