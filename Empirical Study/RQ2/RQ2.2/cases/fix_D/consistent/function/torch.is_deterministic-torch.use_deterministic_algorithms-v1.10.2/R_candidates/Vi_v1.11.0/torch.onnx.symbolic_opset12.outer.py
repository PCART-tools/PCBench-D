@parse_args("v", "v")
def outer(g, input, other):
    # make sure to cast other to self's type
    if other.type().scalarType() != input.type().scalarType():
        other = g.op("Cast", other, to_i=sym_help.cast_pytorch_to_onnx[input.type().scalarType()])
    return einsum_helper(g, "i,j->ij", [input, other])
