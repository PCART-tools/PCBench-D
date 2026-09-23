@_onnx_symbolic("aten::sigmoid")
# Fixed scale and zero_point, discovered from aten/src/ATen/native/quantized/cpu/qsigmoid.cpp
@symbolic_helper.quantized_args(True, scale=1.0 / 256.0, zero_point=0)
def sigmoid(g: jit_utils.GraphContext, self):
    """Converts the corresponding PyTorch function into ONNX operators.

    It is not meant to be called directly by a user.

    Args:
        g (jit_utils.GraphContext): Graph context.
        self (Tensor): the input tensor.
    Returns:
        ONNX operator
    """
    return g.op("Sigmoid", self)
