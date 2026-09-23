def is_floating_point(g, self):
    if sym_help._is_fp(self):
        return g.op("Constant", value_t=torch.BoolTensor([1]))
    return g.op("Constant", value_t=torch.BoolTensor([0]))
