@doc_wraps(scipy.stats.kurtosistest)
def kurtosistest(a, axis=0, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")

    n = float(a.shape[axis])
    b2 = kurtosis(a, axis, fisher=False)

    E = 3.0 * (n - 1) / (n + 1)
    varb2 = 24.0 * n * (n - 2) * (n - 3) / ((n + 1) * (n + 1.) * (n + 3) * (n + 5))  # [1]_ Eq. 1
    x = (b2 - E) / np.sqrt(varb2)  # [1]_ Eq. 4
    # [1]_ Eq. 2:
    sqrtbeta1 = 6.0 * (n * n - 5 * n + 2) / ((n + 7) * (n + 9)) * np.sqrt((6.0 * (n + 3) * (n + 5)) /
                                                                          (n * (n - 2) * (n - 3)))
    # [1]_ Eq. 3:
    A = 6.0 + 8.0 / sqrtbeta1 * (2.0 / sqrtbeta1 + np.sqrt(1 + 4.0 / (sqrtbeta1**2)))
    term1 = 1 - 2 / (9.0 * A)
    denom = 1 + x * np.sqrt(2 / (A - 4.0))
    denom = np.where(denom < 0, 99, denom)
    term2 = np.where(denom < 0, term1, np.power((1 - 2.0 / A) / denom, 1 / 3.0))
    Z = (term1 - term2) / np.sqrt(2 / (9.0 * A))  # [1]_ Eq. 5
    Z = np.where(denom == 99, 0, Z)
    if Z.ndim == 0:
        Z = Z[()]

    # zprob uses upper tail, so Z needs to be positive
    return delayed(KurtosistestResult, nout=2)(Z, 2 * distributions.norm.sf(np.abs(Z)))
