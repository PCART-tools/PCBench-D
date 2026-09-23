def _len(g, self):
    sz_0 = size(g, self, g.op("Constant", value_t=torch.LongTensor([0])))
    return sym_help._squeeze_helper(g, sz_0, [0])
