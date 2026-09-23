def foreach_pow_scalar(scalar, exps):
    return torch._foreach_pow([scalar for _ in exps], exps)
