@parse_args("v", "i", "i", "i")
def unfold(g, input, dimension, size, step):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", input, operator_s="unfold", dimension_i=dimension, size_i=size, step_i=step)
    sizes = sym_help._get_tensor_sizes(input)
    try:
        sizedim = sizes[dimension]
    except Exception:
        sizedim = None
    if sizedim is not None:
        low_indices = range(0, sizedim, step)
        hi_indices = range(size, sizedim + 1, step)
        stack = [sym_help._slice_helper(g, input, axes=[dimension], starts=[low], ends=[hi])
                 for low, hi in zip(low_indices, hi_indices)]
        ndim = len(sizes)
        perm = list(range(0, ndim))
        perm.append(perm.pop(dimension))
        unsqueeze = [sym_help._unsqueeze_helper(g, g.op("Transpose", t, perm_i=perm), [dimension]) for t in stack]
        return g.op("Concat", *unsqueeze, axis_i=dimension)
    else:
        return _unimplemented("Unfold", "input size not accessible")
