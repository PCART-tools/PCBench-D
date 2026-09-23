def linear_prepack(g, weight, bias):
    # Mapping to a dummy caffe2 prepack node.
    # During the onnx -> c2 conversion we can look up original weight and bias
    # from this node
    output = g.op("_caffe2::WeightPrepack", weight, bias)
    sym_help._quantized_ops.add(output)
    return output
