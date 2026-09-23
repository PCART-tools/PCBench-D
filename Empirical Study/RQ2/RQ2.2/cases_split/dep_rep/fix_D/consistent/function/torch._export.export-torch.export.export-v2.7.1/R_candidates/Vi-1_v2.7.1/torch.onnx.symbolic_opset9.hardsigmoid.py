@_onnx_symbolic("aten::hardsigmoid")
# Fixed scale and zero_point, discovered from aten/src/ATen/native/quantized/cpu/qhardsigmoid.cpp
@symbolic_helper.quantized_args(True, scale=1.0 / 256.0, zero_point=0)
@symbolic_helper.parse_args("v")
def hardsigmoid(g: jit_utils.GraphContext, self):
    # Set alpha_f to 1 / 6 to make op equivalent to PyTorch's definition of Hardsigmoid.
    # See https://pytorch.org/docs/stable/generated/torch.nn.Hardsigmoid.html
    return g.op("HardSigmoid", self, alpha_f=1 / 6)
