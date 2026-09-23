def factorial(n, exact=False):
    """
    The factorial of a number or array of numbers.

    The factorial of non-negative integer `n` is the product of all
    positive integers less than or equal to `n`::

        n! = n * (n - 1) * (n - 2) * ... * 1

    Parameters
    ----------
    n : int or array_like of ints
        Input values.  If ``n < 0``, the return value is 0.
    exact : bool, optional
        If True, calculate the answer exactly using long integer arithmetic.
        If False, result is approximated in floating point rapidly using the
        `gamma` function.
        Default is False.

    Returns
    -------
    nf : float or int or ndarray
        Factorial of `n`, as integer or float depending on `exact`.

    Notes
    -----
    For arrays with ``exact=True``, the factorial is computed only once, for
    the largest input, with each other result computed in the process.
    The output dtype is increased to ``int64`` or ``object`` if necessary.

    With ``exact=False`` the factorial is approximated using the gamma
    function:

    .. math:: n! = \Gamma(n+1)

    Examples
    --------
    >>> from scipy.special import factorial
    >>> arr = np.array([3, 4, 5])
    >>> factorial(arr, exact=False)
    array([   6.,   24.,  120.])
    >>> factorial(arr, exact=True)
    array([  6,  24, 120])
    >>> factorial(5, exact=True)
    120L

    """
    if exact:
        if np.ndim(n) == 0:
            return 0 if n < 0 else math.factorial(n)
        else:
            n = asarray(n)
            un = np.unique(n).astype(object)

            # Convert to object array of long ints if np.int can't handle size
            if un[-1] > 20:
                dt = object
            elif un[-1] > 12:
                dt = np.int64
            else:
                dt = np.int

            out = np.empty_like(n, dtype=dt)

            # Handle invalid/trivial values
            un = un[un > 1]
            out[n < 2] = 1
            out[n < 0] = 0

            # Calculate products of each range of numbers
            if un.size:
                val = math.factorial(un[0])
                out[n == un[0]] = val
                for i in xrange(len(un) - 1):
                    prev = un[i] + 1
                    current = un[i + 1]
                    val *= _range_prod(prev, current)
                    out[n == current] = val
            return out
    else:
        n = asarray(n)
        vals = gamma(n + 1)
        return where(n >= 0, vals, 0)
