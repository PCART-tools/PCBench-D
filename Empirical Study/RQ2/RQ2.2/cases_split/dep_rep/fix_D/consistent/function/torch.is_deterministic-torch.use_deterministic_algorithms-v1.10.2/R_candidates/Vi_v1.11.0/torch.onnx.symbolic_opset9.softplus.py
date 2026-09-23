def softplus(g, self, beta, threshold):
    beta_const = sym_help._maybe_get_const(beta, "f")
    if beta_const != 1:
        return g.op("Div", g.op("Softplus", g.op("Mul", self, beta)), beta)
    return g.op("Softplus", self)
