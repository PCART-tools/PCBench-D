@register_kl(Gumbel, Beta)
@register_kl(Gumbel, ContinuousBernoulli)
@register_kl(Gumbel, Exponential)
@register_kl(Gumbel, Gamma)
@register_kl(Gumbel, Pareto)
@register_kl(Gumbel, Uniform)
def _kl_gumbel_infinity(p, q):
    return _infinite_like(p.loc)
