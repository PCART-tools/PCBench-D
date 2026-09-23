@register_kl(Exponential, Beta)
@register_kl(Exponential, ContinuousBernoulli)
@register_kl(Exponential, Pareto)
@register_kl(Exponential, Uniform)
def _kl_exponential_infinity(p, q):
    return _infinite_like(p.rate)
