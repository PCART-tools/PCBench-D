@_onnx_symbolic("aten::round")
@symbolic_helper.parse_args("v", "i")
def round(g: jit_utils.GraphContext, self, decimals=0):
    if not symbolic_helper._is_fp(self):
        return self
    if decimals == 0:
        return g.op("Round", self)
    mul = g.op("Mul", self, g.op("Constant", value_t=torch.tensor(pow(10, decimals))))
    round = g.op("Round", mul)
    return g.op(
        "Mul", round, g.op("Constant", value_t=torch.tensor(pow(10, -1 * decimals)))
    )
