@_onnx_symbolic("aten::masked_fill")
def masked_fill(g: jit_utils.GraphContext, self, mask, value):
    """Implement the masked_fill functionality available for a pytorch tensor in ONNX.

    Fills elements of the input tensor with `value` where `mask` is True.
    """
    mask = g.op("Cast", mask, to_i=_C_onnx.TensorProtoDataType.BOOL)
    value = symbolic_helper._maybe_get_scalar(value)
    return g.op("Where", mask, symbolic_helper._if_scalar_type_as(value, self), self)
