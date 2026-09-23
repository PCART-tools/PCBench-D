def __isnot_(g, self, other):
    if sym_help._is_none(other):
        if sym_help._is_none(self):
            return g.op("Constant", value_t=torch.BoolTensor([0]))
        return g.op("Constant", value_t=torch.BoolTensor([1]))
    return ne(g, self, other)
