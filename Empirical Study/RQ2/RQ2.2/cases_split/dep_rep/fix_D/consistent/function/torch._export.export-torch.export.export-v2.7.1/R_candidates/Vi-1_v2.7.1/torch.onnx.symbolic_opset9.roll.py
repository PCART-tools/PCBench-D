@_onnx_symbolic("aten::roll")
@symbolic_helper.parse_args("v", "is", "is")
def roll(g: jit_utils.GraphContext, self, shifts, dims):
    assert len(shifts) == len(dims)

    result = self
    for i in range(len(shifts)):
        shapes = []
        shape = symbolic_helper._slice_helper(
            g, result, axes=[dims[i]], starts=[-shifts[i]], ends=[sys.maxsize]
        )
        shapes.append(shape)
        shape = symbolic_helper._slice_helper(
            g, result, axes=[dims[i]], starts=[0], ends=[-shifts[i]]
        )
        shapes.append(shape)
        result = g.op("Concat", *shapes, axis_i=dims[i])

    return result
