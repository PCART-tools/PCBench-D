def entropy(pk, qk=None, base=None):
    """Calculate the entropy of a distribution for given probability values.

    If only probabilities `pk` are given, the entropy is calculated as
    ``S = -sum(pk * log(pk), axis=0)``.

    If `qk` is not None, then compute a relative entropy (also known as
    Kullback-Leibler divergence or Kullback-Leibler distance)
    ``S = sum(pk * log(pk / qk), axis=0)``.

    This routine will normalize `pk` and `qk` if they don't sum to 1.

    Parameters
    ----------
    pk : sequence
        Defines the (discrete) distribution. ``pk[i]`` is the (possibly
        unnormalized) probability of event ``i``.
    qk : sequence, optional
        Sequence against which the relative entropy is computed. Should be in
        the same format as `pk`.
    base : float, optional
        The logarithmic base to use, defaults to ``e`` (natural logarithm).

    Returns
    -------
    S : float
        The calculated entropy.

    """
    pk = asarray(pk)
    pk = 1.0*pk / sum(pk, axis=0)
    if qk is None:
        vec = special.xlogy(pk, pk)
    else:
        qk = asarray(qk)
        if len(qk) != len(pk):
            raise ValueError("qk and pk must have same length.")
        qk = 1.0*qk / sum(qk, axis=0)
        # If qk is zero anywhere, then unless pk is zero at those places
        #   too, the relative entropy is infinite.
        if any(take(pk, nonzero(qk == 0.0), axis=0) != 0.0, 0):
            return inf
        vec = -special.xlogy(pk, pk / qk)
    S = -sum(vec, axis=0)
    if base is not None:
        S /= log(base)
    return S
