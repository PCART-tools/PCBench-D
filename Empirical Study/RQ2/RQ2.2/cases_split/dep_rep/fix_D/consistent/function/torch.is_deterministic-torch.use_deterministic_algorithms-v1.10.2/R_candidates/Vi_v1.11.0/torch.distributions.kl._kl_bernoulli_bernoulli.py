@register_kl(Bernoulli, Bernoulli)
def _kl_bernoulli_bernoulli(p, q):
    t1 = p.probs * (p.probs / q.probs).log()
    t1[q.probs == 0] = inf
    t1[p.probs == 0] = 0
    t2 = (1 - p.probs) * ((1 - p.probs) / (1 - q.probs)).log()
    t2[q.probs == 1] = inf
    t2[p.probs == 1] = 0
    return t1 + t2
