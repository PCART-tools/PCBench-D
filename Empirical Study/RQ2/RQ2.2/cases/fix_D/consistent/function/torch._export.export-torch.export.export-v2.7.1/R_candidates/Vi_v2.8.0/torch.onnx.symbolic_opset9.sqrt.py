@_onnx_symbolic("aten::sqrt")
def sqrt(g: jit_utils.GraphContext, self):
    if _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.UNDEFINED
    ) in {
        _type_utils.JitScalarType.UINT8,
        _type_utils.JitScalarType.INT8,
        _type_utils.JitScalarType.INT16,
        _type_utils.JitScalarType.INT,
        _type_utils.JitScalarType.INT64,
    }:
        # torch converts all int inputs to sqrt to float
        self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.FLOAT)

    return g.op("Sqrt", self)
