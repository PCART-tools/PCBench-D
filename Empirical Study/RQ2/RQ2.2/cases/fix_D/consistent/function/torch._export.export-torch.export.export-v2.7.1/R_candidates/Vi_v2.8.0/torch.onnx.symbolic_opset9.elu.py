@_onnx_symbolic("aten::elu")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "t", "t", "t")
def elu(g: jit_utils.GraphContext, input, alpha, scale, input_scale):
    if scale and scale != 1.0:
        return symbolic_helper._unimplemented(
            "scale", "does not support scale in Elu", scale
        )
    if input_scale and input_scale != 1.0:
        return symbolic_helper._unimplemented(
            "input_scale", "does not support input_scale in Elu", input_scale
        )
    # See Note [Export inplace]
    return g.op("Elu", input, alpha_f=symbolic_helper._scalar(alpha))
