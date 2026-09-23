def rsqrt(g, self):
    return g.op("Div", sym_help._if_scalar_type_as(g, torch.ones(1), self), sqrt(g, self))
