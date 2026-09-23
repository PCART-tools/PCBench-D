@array_function_dispatch(_binary_op_dispatcher)
def polyadd(a1, a2):
    """
    Find the sum of two polynomials.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Returns the polynomial resulting from the sum of two input polynomials.
    Each input must be either a poly1d object or a 1D sequence of polynomial
    coefficients, from highest to lowest degree.

    Parameters
    ----------
    a1, a2 : array_like or poly1d object
        Input polynomials.

    Returns
    -------
    out : ndarray or poly1d object
        The sum of the inputs. If either input is a poly1d object, then the
        output is also a poly1d object. Otherwise, it is a 1D array of
        polynomial coefficients from highest to lowest degree.

    See Also
    --------
    poly1d : A one-dimensional polynomial class.
    poly, polyadd, polyder, polydiv, polyfit, polyint, polysub, polyval

    Examples
    --------
    >>> np.polyadd([1, 2], [9, 5, 4])
    array([9, 6, 6])

    Using poly1d objects:

    >>> p1 = np.poly1d([1, 2])
    >>> p2 = np.poly1d([9, 5, 4])
    >>> print(p1)
    1 x + 2
    >>> print(p2)
       2
    9 x + 5 x + 4
    >>> print(np.polyadd(p1, p2))
       2
    9 x + 6 x + 6

    """
    truepoly = (isinstance(a1, poly1d) or isinstance(a2, poly1d))
    a1 = atleast_1d(a1)
    a2 = atleast_1d(a2)
    diff = len(a2) - len(a1)
    if diff == 0:
        val = a1 + a2
    elif diff > 0:
        zr = NX.zeros(diff, a1.dtype)
        val = NX.concatenate((zr, a1)) + a2
    else:
        zr = NX.zeros(abs(diff), a2.dtype)
        val = a1 + NX.concatenate((zr, a2))
    if truepoly:
        val = poly1d(val)
    return val
