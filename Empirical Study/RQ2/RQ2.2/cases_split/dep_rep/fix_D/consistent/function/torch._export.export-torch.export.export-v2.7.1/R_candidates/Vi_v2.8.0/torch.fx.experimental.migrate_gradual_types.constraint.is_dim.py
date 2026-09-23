def is_dim(d):
    return isinstance(d, (DVar, int)) or d == Dyn
