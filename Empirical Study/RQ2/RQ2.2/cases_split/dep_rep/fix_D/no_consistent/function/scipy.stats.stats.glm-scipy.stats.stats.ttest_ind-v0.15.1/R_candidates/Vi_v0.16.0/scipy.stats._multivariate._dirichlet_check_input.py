def _dirichlet_check_input(alpha, x):
    x = np.asarray(x)

    if x.shape[0] + 1 != alpha.shape[0] and x.shape[0] != alpha.shape[0]:
        raise ValueError("Vector 'x' must have one entry less then the" +
                         " parameter vector 'a', but alpha.shape = " +
                         "%s and " % alpha.shape +
                         "x.shape = %s." % x.shape)

    if x.shape[0] != alpha.shape[0]:
        xk = np.array([1 - np.sum(x, 0)])
        if xk.ndim == 1:
            x = np.append(x, xk)
        elif xk.ndim == 2:
            x = np.vstack((x, xk))
        else:
            raise ValueError("The input must be one dimensional or a two "
                             "dimensional matrix containing the entries.")

    if np.min(x) < 0:
        raise ValueError("Each entry in 'x' must be greater or equal zero.")

    if np.max(x) > 1:
        raise ValueError("Each entry in 'x' must be smaller or equal one.")

    if (np.abs(np.sum(x, 0) - 1.0) > 10e-10).any():
        raise ValueError("The input vector 'x' must lie within the normal " +
                         "simplex. but sum(x)=%f." % np.sum(x, 0))

    return x
