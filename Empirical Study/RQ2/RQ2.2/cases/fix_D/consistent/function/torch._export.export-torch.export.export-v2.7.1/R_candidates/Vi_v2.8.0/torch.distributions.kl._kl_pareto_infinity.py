@register_kl(Pareto, Beta)
@register_kl(Pareto, ContinuousBernoulli)
@register_kl(Pareto, Uniform)
def _kl_pareto_infinity(p, q):
    return _infinite_like(p.scale)
