def _any(g, input):
    input = _cast_Long(g, input, False)  # type: ignore[name-defined]
    input_sum = sym_help._reducesum_helper(g, input, keepdims_i=0)
    return gt(g, input_sum, g.op("Constant", value_t=torch.LongTensor([0])))
