def _var_combine(g, levels):
    return g.groupby(level=levels, sort=False).sum()
