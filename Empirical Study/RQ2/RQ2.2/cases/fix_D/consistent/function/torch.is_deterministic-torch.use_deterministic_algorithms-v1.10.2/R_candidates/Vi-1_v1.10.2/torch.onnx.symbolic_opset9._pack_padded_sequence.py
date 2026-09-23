@parse_args("v", "v", "i")
def _pack_padded_sequence(g, input, lengths, batch_first):
    # There currently is no PackPadded operator in ONNX. We rely on an
    # optimization pass to remove this later. It is an error if all
    # PackPadded operators cannot be optimized out.
    if batch_first:
        input = g.op("Transpose", input, perm_i=[1, 0, 2])
    if not lengths.type().isSubtypeOf(torch._C.TensorType.get()):
        raise RuntimeError("Lengths must be a Tensor for ONNX export")
    # We know it's a TensorType so this check is now safe.
    # It's really only necessary because those operators expand to something that
    # only works with int32 types in Caffe2...
    if lengths.type().scalarType() != "Int":
        lengths = _cast_Int(g, lengths, False)  # type: ignore[name-defined]
    return g.op("prim::PackPadded", input, lengths, outputs=2)
