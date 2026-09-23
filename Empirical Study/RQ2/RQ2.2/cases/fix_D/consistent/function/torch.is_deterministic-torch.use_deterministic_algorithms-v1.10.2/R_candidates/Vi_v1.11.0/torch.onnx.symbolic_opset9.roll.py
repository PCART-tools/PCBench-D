@parse_args("v", "is", "is")
def roll(g, self, shifts, dims):
    assert len(shifts) == len(dims)

    result = self
    for i in range(len(shifts)):
        shapes = []
        shape = sym_help._slice_helper(g,
                                       result,
                                       axes=[dims[i]],
                                       starts=[-shifts[i]],
                                       ends=[maxsize])
        shapes.append(shape)
        shape = sym_help._slice_helper(g,
                                       result,
                                       axes=[dims[i]],
                                       starts=[0],
                                       ends=[-shifts[i]])
        shapes.append(shape)
        result = g.op("Concat", *shapes, axis_i=dims[i])

    return result
