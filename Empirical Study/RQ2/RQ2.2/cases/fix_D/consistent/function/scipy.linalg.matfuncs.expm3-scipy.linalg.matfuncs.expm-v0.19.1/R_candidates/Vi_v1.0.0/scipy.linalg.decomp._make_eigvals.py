def _make_eigvals(alpha, beta, homogeneous_eigvals):
    if homogeneous_eigvals:
        if beta is None:
            return numpy.vstack((alpha, numpy.ones_like(alpha)))
        else:
            return numpy.vstack((alpha, beta))
    else:
        if beta is None:
            return alpha
        else:
            w = numpy.empty_like(alpha)
            alpha_zero = (alpha == 0)
            beta_zero = (beta == 0)
            beta_nonzero = ~beta_zero
            w[beta_nonzero] = alpha[beta_nonzero]/beta[beta_nonzero]
            # Use numpy.inf for complex values too since
            # 1/numpy.inf = 0, i.e. it correctly behaves as projective
            # infinity.
            w[~alpha_zero & beta_zero] = numpy.inf
            if numpy.all(alpha.imag == 0):
                w[alpha_zero & beta_zero] = numpy.nan
            else:
                w[alpha_zero & beta_zero] = complex(numpy.nan, numpy.nan)
            return w
