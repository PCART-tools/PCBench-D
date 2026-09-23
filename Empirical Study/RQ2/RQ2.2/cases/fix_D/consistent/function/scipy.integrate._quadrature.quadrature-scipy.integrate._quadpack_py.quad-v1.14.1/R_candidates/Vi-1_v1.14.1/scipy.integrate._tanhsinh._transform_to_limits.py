def _transform_to_limits(xjc, wj, a, b):
    # Transform integral according to user-specified limits. This is just
    # math that follows from the fact that the standard limits are (-1, 1).
    # Note: If we had stored xj instead of xjc, we would have
    # xj = alpha * xj + beta, where beta = (a + b)/2
    alpha = (b - a) / 2
    xj = np.concatenate((-alpha * xjc + b, alpha * xjc + a), axis=-1)
    wj = wj*alpha  # arguments get broadcasted, so we can't use *=
    wj = np.concatenate((wj, wj), axis=-1)

    # Points at the boundaries can be generated due to finite precision
    # arithmetic, but these function values aren't supposed to be included in
    # the Euler-Maclaurin sum. Ideally we wouldn't evaluate the function at
    # these points; however, we can't easily filter out points since this
    # function is vectorized. Instead, zero the weights.
    invalid = (xj <= a) | (xj >= b)
    wj[invalid] = 0
    return xj, wj
