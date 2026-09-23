def __getitem_(g, self, i):
    return select(g, self, g.op("Constant", value_t=torch.tensor([0])), i)
