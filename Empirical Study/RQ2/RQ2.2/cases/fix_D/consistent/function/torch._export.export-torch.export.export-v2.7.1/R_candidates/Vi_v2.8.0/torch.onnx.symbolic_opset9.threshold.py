@_onnx_symbolic("aten::threshold")
@symbolic_helper.parse_args("v", "t", "t")
def threshold(g: jit_utils.GraphContext, self, threshold, value):
    # See Note [Export inplace]
    if symbolic_helper._scalar(threshold) != 0:
        return symbolic_helper._unimplemented("threshold", "non-zero threshold", self)
    if symbolic_helper._scalar(value) != 0:
        return symbolic_helper._unimplemented("threshold", "non-zero value", self)
    return g.op("Relu", self)
