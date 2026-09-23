@_onnx_symbolic("aten::unfold")
@symbolic_helper.parse_args("v", "i", "i", "i")
def unfold(g: jit_utils.GraphContext, input, dimension, size, step):
    sizes = symbolic_helper._get_tensor_sizes(input)
    # FIXME(justinchuby): Get rid of the try catch here to improve readability
    try:
        sizedim = sizes[dimension]
    except Exception:
        # FIXME(justinchuby): Avoid catching Exception.
        # Catch a more specific exception instead.
        sizedim = None
    if sizedim is not None:
        low_indices = range(0, sizedim, step)
        hi_indices = range(size, sizedim + 1, step)
        stack = [
            symbolic_helper._slice_helper(
                g, input, axes=[dimension], starts=[low], ends=[hi]
            )
            for low, hi in zip(low_indices, hi_indices)
        ]
        ndim = len(sizes)
        perm = list(range(0, ndim))
        perm.append(perm.pop(dimension))
        unsqueeze = [
            symbolic_helper._unsqueeze_helper(
                g, g.op("Transpose", t, perm_i=perm), [dimension]
            )
            for t in stack
        ]
        return g.op("Concat", *unsqueeze, axis_i=dimension)
    else:
        return symbolic_helper._unimplemented(
            "Unfold", "input size not accessible", input
        )
