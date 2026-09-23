@_onnx_symbolic("aten::one_hot")
def one_hot(g: jit_utils.GraphContext, self, num_classes):
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    # onnxruntime supports limited type combinations for OneHot.
    if _type_utils.JitScalarType.from_value(
        num_classes, _type_utils.JitScalarType.UNDEFINED
    ) in {
        _type_utils.JitScalarType.UINT8,
        _type_utils.JitScalarType.INT8,
        _type_utils.JitScalarType.INT,
        _type_utils.JitScalarType.INT16,
    }:
        num_classes = g.op("Cast", num_classes, to_i=_C_onnx.TensorProtoDataType.INT64)
    return g.op("OneHot", self, num_classes, values, axis_i=-1)
