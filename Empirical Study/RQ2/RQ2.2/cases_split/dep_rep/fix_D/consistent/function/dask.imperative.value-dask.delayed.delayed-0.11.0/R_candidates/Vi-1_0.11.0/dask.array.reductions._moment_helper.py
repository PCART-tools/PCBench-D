def _moment_helper(Ms, ns, inner_term, order, sum, kwargs):
    M = Ms[..., order - 2].sum(**kwargs) + sum(ns * inner_term**order, **kwargs)
    for k in range(1, order - 1):
        coeff = factorial(order)/(factorial(k)*factorial(order - k))
        M += coeff * sum(Ms[..., order - k - 2] * inner_term**k, **kwargs)
    return M
