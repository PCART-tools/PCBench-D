@register_kl(Normal, Beta)
@register_kl(Normal, ContinuousBernoulli)
@register_kl(Normal, Exponential)
@register_kl(Normal, Gamma)
@register_kl(Normal, Pareto)
@register_kl(Normal, Uniform)
def _kl_normal_infinity(p, q):
    return _infinite_like(p.loc)
