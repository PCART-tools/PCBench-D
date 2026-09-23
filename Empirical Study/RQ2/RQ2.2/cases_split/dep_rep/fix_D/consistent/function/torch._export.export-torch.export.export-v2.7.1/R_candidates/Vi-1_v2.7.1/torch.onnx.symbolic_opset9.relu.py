@_onnx_symbolic("aten::relu")
@symbolic_helper.quantized_args(True)
def relu(g: jit_utils.GraphContext, input):
    return symbolic_helper._op_with_optional_float_cast(
        g, "Relu", input, opset_before=14
    )
