def mm(g, self, other):
    return g.op("Gemm", self, other, beta_f=0.0, alpha_f=1.0)
