def chebyu(n, monic=False):
    """Return nth order Chebyshev polynomial of second kind, Un(x).  Orthogonal
    over [-1,1] with weight function (1-x**2)**(1/2).
    """
    base = jacobi(n, 0.5, 0.5, monic=monic)
    if monic:
        return base
    factor = sqrt(pi) / 2.0 * _gam(n + 2) / _gam(n + 1.5)
    base._scale(factor)
    return base
