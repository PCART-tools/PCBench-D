@_onnx_symbolic("aten::_pack_padded_sequence")
@symbolic_helper.parse_args("v", "v", "i")
def _pack_padded_sequence(g: jit_utils.GraphContext, input, lengths, batch_first):
    # Currently there is no PackPadded operator in ONNX. We rely on an
    # optimization pass to remove this later. It is an error if all
    # PackPadded operators cannot be optimized out.
    if batch_first:
        input = g.op("Transpose", input, perm_i=[1, 0, 2])
    if not lengths.type().isSubtypeOf(torch._C.TensorType.get()):
        raise errors.SymbolicValueError(
            "'lengths' must be a Tensor for ONNX export", input
        )
    # We know it's a TensorType so this check is now safe.
    # It's really only necessary because those operators expand to something that
    # only works with int32 types in Caffe2...
    if (
        _type_utils.JitScalarType.from_value(
            lengths, _type_utils.JitScalarType.UNDEFINED
        )
        != _type_utils.JitScalarType.INT
    ):
        lengths = g.op("Cast", lengths, to_i=_C_onnx.TensorProtoDataType.INT32)
    return g.op("prim::PackPadded", input, lengths, outputs=2)
