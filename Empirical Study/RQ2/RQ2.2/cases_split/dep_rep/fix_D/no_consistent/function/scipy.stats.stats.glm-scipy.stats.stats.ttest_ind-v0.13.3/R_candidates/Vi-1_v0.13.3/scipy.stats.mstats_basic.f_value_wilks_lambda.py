def f_value_wilks_lambda(ER, EF, dfnum, dfden, a, b):
    """Calculation of Wilks lambda F-statistic for multivarite data, per
    Maxwell & Delaney p.657.
    """
    ER = ma.array(ER, copy=False, ndmin=2)
    EF = ma.array(EF, copy=False, ndmin=2)
    if ma.getmask(ER).any() or ma.getmask(EF).any():
        raise NotImplementedError("Not implemented when the inputs "
                                  "have missing data")
    lmbda = np.linalg.det(EF) / np.linalg.det(ER)
    q = ma.sqrt(((a-1)**2*(b-1)**2 - 2) / ((a-1)**2 + (b-1)**2 - 5))
    q = ma.filled(q, 1)
    n_um = (1 - lmbda**(1.0/q))*(a-1)*(b-1)
    d_en = lmbda**(1.0/q) / (n_um*q - 0.5*(a-1)*(b-1) + 1)
    return n_um / d_en
