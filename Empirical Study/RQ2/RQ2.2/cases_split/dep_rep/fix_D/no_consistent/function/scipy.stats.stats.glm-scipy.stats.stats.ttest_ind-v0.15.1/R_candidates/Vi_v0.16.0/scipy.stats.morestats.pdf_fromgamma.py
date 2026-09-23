@np.deprecate(message="scipy.stats.pdf_fromgamma is deprecated in scipy 0.16.0 "
                      "in favour of statsmodels.distributions.ExpandedNormal.")
def pdf_fromgamma(g1, g2, g3=0.0, g4=None):
    if g4 is None:
        g4 = 3 * g2**2
    sigsq = 1.0 / g2
    sig = sqrt(sigsq)
    mu = g1 * sig**3.0
    p12 = _hermnorm(13)
    for k in range(13):
        p12[k] /= sig**k

    # Add all of the terms to polynomial
    totp = (p12[0] - g1/6.0*p12[3] +
            g2/24.0*p12[4] + g1**2/72.0 * p12[6] -
            g3/120.0*p12[5] - g1*g2/144.0*p12[7] - g1**3.0/1296.0*p12[9] +
            g4/720*p12[6] + (g2**2/1152.0 + g1*g3/720)*p12[8] +
            g1**2 * g2/1728.0*p12[10] + g1**4.0 / 31104.0*p12[12])
    # Final normalization
    totp = totp / sqrt(2*pi) / sig

    def thefunc(x):
        xn = (x - mu) / sig
        return totp(xn) * exp(-xn**2 / 2.)

    return thefunc
