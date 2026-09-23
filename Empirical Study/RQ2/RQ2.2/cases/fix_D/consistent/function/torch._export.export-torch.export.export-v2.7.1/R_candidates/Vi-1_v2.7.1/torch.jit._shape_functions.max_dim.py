def max_dim(self: list[int], dim: int, keep_dim: bool):
    out = sum_mean_dim(self, [dim], keep_dim, None)
    return out, out
