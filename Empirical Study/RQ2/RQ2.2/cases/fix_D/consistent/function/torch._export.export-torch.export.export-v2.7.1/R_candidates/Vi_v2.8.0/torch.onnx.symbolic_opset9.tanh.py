@_onnx_symbolic("aten::tanh")
# Fixed scale and zero_point, discovered from aten/src/ATen/native/quantized/cpu/qtanh.cpp
@symbolic_helper.quantized_args(True, scale=2.0 / 256.0, zero_point=128)
def tanh(g: jit_utils.GraphContext, self):
    return g.op("Tanh", self)
