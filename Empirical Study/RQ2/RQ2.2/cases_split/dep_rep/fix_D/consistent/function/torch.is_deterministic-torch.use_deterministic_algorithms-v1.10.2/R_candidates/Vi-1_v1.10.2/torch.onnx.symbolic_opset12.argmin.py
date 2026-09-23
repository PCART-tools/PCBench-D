def argmin(g, input, dim, keepdim):
    if sym_help._is_none(dim):
        flattened = sym_help._reshape_helper(g, input, g.op("Constant", value_t=torch.tensor([-1])))
        return g.op("ArgMin", flattened, axis_i=0, keepdims_i=False, select_last_index_i=False)
    else:
        dim = _parse_arg(dim, "i")
        keepdim = _parse_arg(keepdim, "i")
        return g.op("ArgMin", input, axis_i=dim, keepdims_i=keepdim, select_last_index_i=False)
