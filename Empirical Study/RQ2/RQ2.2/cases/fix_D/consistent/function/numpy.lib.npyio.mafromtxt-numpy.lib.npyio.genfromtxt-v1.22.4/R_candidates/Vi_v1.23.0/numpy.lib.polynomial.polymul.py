@array_function_dispatch(_binary_op_dispatcher)
def polymul(a1, a2):
    """
    Find the product of two polynomials.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Finds the polynomial resulting from the multiplication of the two input
    polynomials. Each input must be either a poly1d object or a 1D sequence
    of polynomial coefficients, from highest to lowest degree.

    Parameters
    ----------
    a1, a2 : array_like or poly1d object
        Input polynomials.

    Returns
    -------
    out : ndarray or poly1d object
        The polynomial resulting from the multiplication of the inputs. If
        either inputs is a poly1d object, then the output is also a poly1d
        object. Otherwise, it is a 1D array of polynomial coefficients from
        highest to lowest degree.

    See Also
    --------
    poly1d : A one-dimensional polynomial class.
    poly, polyadd, polyder, polydiv, polyfit, polyint, polysub, polyval
    convolve : Array convolution. Same output as polymul, but has parameter
               for overlap mode.

    Examples
    --------
    >>> np.polymul([1, 2, 3], [9, 5, 1])
    array([ 9, 23, 38, 17,  3])

    Using poly1d objects:

    >>> p1 = np.poly1d([1, 2, 3])
    >>> p2 = np.poly1d([9, 5, 1])
    >>> print(p1)
       2
    1 x + 2 x + 3
    >>> print(p2)
       2
    9 x + 5 x + 1
    >>> print(np.polymul(p1, p2))
       4      3      2
    9 x + 23 x + 38 x + 17 x + 3

    """
    truepoly = (isinstance(a1, poly1d) or isinstance(a2, poly1d))
    a1, a2 = poly1d(a1), poly1d(a2)
    val = NX.convolve(a1, a2)
    if truepoly:
        val = poly1d(val)
    return val
