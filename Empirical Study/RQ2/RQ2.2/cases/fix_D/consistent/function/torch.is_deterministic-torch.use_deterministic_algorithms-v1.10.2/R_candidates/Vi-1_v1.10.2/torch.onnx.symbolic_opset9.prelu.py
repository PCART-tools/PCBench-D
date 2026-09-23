def prelu(g, self, weight):
    self_rank = sym_help._get_tensor_rank(self)
    if self_rank is not None and self_rank > 2:
        weight = sym_help._unsqueeze_helper(g, weight, list(range(1, self_rank - 1)))
    return g.op("PRelu", self, weight)
