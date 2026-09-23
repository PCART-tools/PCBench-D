def log1p(g, self):
    return log(g, add(g, sym_help._if_scalar_type_as(g, torch.ones(1), self), self))
