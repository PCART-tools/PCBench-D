@symbolic_helper.parse_args("v")
def dequantize(g: jit_utils.GraphContext, input):
    return g.op("_caffe2::Int8Dequantize", input)
