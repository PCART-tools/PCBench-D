def t(g, self):
    return g.op("Transpose", self, perm_i=(1, 0))
