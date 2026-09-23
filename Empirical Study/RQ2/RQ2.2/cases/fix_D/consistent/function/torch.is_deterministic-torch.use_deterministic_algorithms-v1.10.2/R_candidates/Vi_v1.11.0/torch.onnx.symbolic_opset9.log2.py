def log2(g, self):
    _ln2 = 0.693147180559945309
    return g.op("Div", log(g, self), g.op("Constant", value_t=torch.tensor([_ln2])))
