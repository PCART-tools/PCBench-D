def leaky_relu(g, input, negative_slope, inplace=False):
    negative_slope = sym_help._get_const(negative_slope, "t", "negative_slope")
    # See Note [Export inplace]
    # TODO: Talk to ONNX about unconditional cast of scalar to float
    return g.op("LeakyRelu", input, alpha_f=sym_help._scalar(negative_slope))
