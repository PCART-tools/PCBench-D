def gelu(g, self):
    _sqrt2 = 1.4142135623730951
    erf = g.op("Erf", g.op("Div", self, torch.tensor(_sqrt2, dtype=torch.double)))
    erf_plusone = add(g, erf, g.op("Constant", value_t=torch.tensor(1, dtype=torch.double)))
    return mul(g, mul(g, self, erf_plusone), g.op("Constant", value_t=torch.tensor(0.5, dtype=torch.double)))
