@_onnx_symbolic("aten::addcmul")
@symbolic_helper.parse_args("v", "v", "v", "f")
def addcmul(g: jit_utils.GraphContext, self, tensor1, tensor2, value=1.0):
    value_tens = g.op("Constant", value_t=torch.tensor([value]))
    return add(g, self, mul(g, mul(g, tensor1, tensor2), value_tens))
