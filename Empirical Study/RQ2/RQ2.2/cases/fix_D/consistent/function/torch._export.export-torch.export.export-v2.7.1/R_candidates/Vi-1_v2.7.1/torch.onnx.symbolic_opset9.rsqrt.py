@_onnx_symbolic("aten::rsqrt")
def rsqrt(g: jit_utils.GraphContext, self):
    return g.op(
        "Div", symbolic_helper._if_scalar_type_as(torch.ones(1), self), sqrt(g, self)
    )
