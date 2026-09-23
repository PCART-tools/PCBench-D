def conv_prepack(
    g: jit_utils.GraphContext, input, weight, bias, stride, padding, dilation, groups
):
    # Mapping to a dummy caffe2 prepack node.
    # During the onnx -> c2 conversion we can look up original weight and bias
    # from this node
    output = g.op("_caffe2::WeightPrepack", input, weight, bias)
    symbolic_helper._quantized_ops.add(output)
    return output
