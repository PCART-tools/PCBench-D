def _from_derivatives(xi, yi, x, order=None, der=0, extrapolate=False):
    """
    Convenience function for interpolate.BPoly.from_derivatives

    Construct a piecewise polynomial in the Bernstein basis, compatible
    with the specified values and derivatives at breakpoints.

    Parameters
    ----------
    xi : array_like
        sorted 1D array of x-coordinates
    yi : array_like or list of array-likes
        yi[i][j] is the j-th derivative known at xi[i]
    orders : None or int or array_like of ints. Default: None.
        Specifies the degree of local polynomials. If not None, some
        derivatives are ignored.
    der : int or list
        How many derivatives to extract; None for all potentially nonzero
        derivatives (that is a number equal to the number of points), or a
        list of derivatives to extract. This numberincludes the function
        value as 0th derivative.
     extrapolate : bool, optional
        Whether to extrapolate to ouf-of-bounds points based on first and last
        intervals, or to return NaNs. Default: True.

    See Also
    --------
    scipy.interpolate.BPoly.from_derivatives

    Returns
    -------
    y : scalar or array_like
        The result, of length R or length M or M by R,

    """
    import scipy
    from scipy import interpolate

    if LooseVersion(scipy.__version__) < '0.18.0':
        try:
            method = interpolate.piecewise_polynomial_interpolate
            return method(xi, yi.reshape(-1, 1), x,
                          orders=order, der=der)
        except AttributeError:
            pass

    # return the method for compat with scipy version & backwards compat
    method = interpolate.BPoly.from_derivatives
    m = method(xi, yi.reshape(-1, 1),
               orders=order, extrapolate=extrapolate)

    return m(x)
