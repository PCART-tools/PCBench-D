def _compute_numerical_gradient(fn, entry, v, norm_v, nbhd_checks_fn):
    # Performs finite differencing by perturbing `entry` in-place by `v` and
    # returns the gradient of each of the outputs wrt to x at idx.
    orig = entry.clone()
    entry.copy_(orig - v)
    outa = fn()
    entry.copy_(orig + v)
    outb = fn()
    entry.copy_(orig)

    def compute(a, b):
        nbhd_checks_fn(a, b)
        ret = (b - a) / (2 * norm_v)
        return ret.detach().reshape(-1)

    return tuple(compute(a, b) for (a, b) in zip(outa, outb))
