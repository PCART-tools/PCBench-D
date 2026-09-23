def _lognorm_logpdf(x, s):
    return -log(x)**2 / (2*s**2) + np.where(x == 0, 0, -log(s*x*sqrt(2*pi)))
