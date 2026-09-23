def reciprocal(g, self):
    return g.op("Div", torch.ones(1), self)
