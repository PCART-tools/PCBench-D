@parse_args("v")
def bitwise_not(g, inp):
    if inp.type().scalarType() != "Bool":
        return _unimplemented("bitwise_not", "non-bool tensor")
    return g.op("Not", inp)
