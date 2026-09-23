@_onnx_symbolic("aten::leaky_relu")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "f", "b")
def leaky_relu(
    g: jit_utils.GraphContext,
    input: _C.Value,
    negative_slope: float,
    inplace: bool = False,
):
    # See Note [Export inplace]
    return g.op("LeakyRelu", input, alpha_f=negative_slope)
