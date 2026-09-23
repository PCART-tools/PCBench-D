def _any(g, *args):
    # aten::any(Tensor self)
    if len(args) == 1:
        input = args[0]
        dim, keepdim = None, 0
    # aten::any(Tensor self, int dim, bool keepdim)
    else:
        input, dim, keepdim = args
        dim = [_parse_arg(dim, "i")]
        keepdim = _parse_arg(keepdim, "i")
    input = _cast_Long(g, input, False)  # type: ignore[name-defined]
    input_sum = sym_help._reducesum_helper(g, input,
                                           axes_i=dim, keepdims_i=keepdim)
    return gt(g, input_sum, g.op("Constant", value_t=torch.LongTensor([0])))
