@array_function_dispatch(_kron_dispatcher)
def kron(a, b):
    """
    Kronecker product of two arrays.

    Computes the Kronecker product, a composite array made of blocks of the
    second array scaled by the first.

    Parameters
    ----------
    a, b : array_like

    Returns
    -------
    out : ndarray

    See Also
    --------
    outer : The outer product

    Notes
    -----
    The function assumes that the number of dimensions of `a` and `b`
    are the same, if necessary prepending the smallest with ones.
    If ``a.shape = (r0,r1,..,rN)`` and ``b.shape = (s0,s1,...,sN)``,
    the Kronecker product has shape ``(r0*s0, r1*s1, ..., rN*SN)``.
    The elements are products of elements from `a` and `b`, organized
    explicitly by::

        kron(a,b)[k0,k1,...,kN] = a[i0,i1,...,iN] * b[j0,j1,...,jN]

    where::

        kt = it * st + jt,  t = 0,...,N

    In the common 2-D case (N=1), the block structure can be visualized::

        [[ a[0,0]*b,   a[0,1]*b,  ... , a[0,-1]*b  ],
         [  ...                              ...   ],
         [ a[-1,0]*b,  a[-1,1]*b, ... , a[-1,-1]*b ]]


    Examples
    --------
    >>> np.kron([1,10,100], [5,6,7])
    array([  5,   6,   7, ..., 500, 600, 700])
    >>> np.kron([5,6,7], [1,10,100])
    array([  5,  50, 500, ...,   7,  70, 700])

    >>> np.kron(np.eye(2), np.ones((2,2)))
    array([[1.,  1.,  0.,  0.],
           [1.,  1.,  0.,  0.],
           [0.,  0.,  1.,  1.],
           [0.,  0.,  1.,  1.]])

    >>> a = np.arange(100).reshape((2,5,2,5))
    >>> b = np.arange(24).reshape((2,3,4))
    >>> c = np.kron(a,b)
    >>> c.shape
    (2, 10, 6, 20)
    >>> I = (1,3,0,2)
    >>> J = (0,2,1)
    >>> J1 = (0,) + J             # extend to ndim=4
    >>> S1 = (1,) + b.shape
    >>> K = tuple(np.array(I) * np.array(S1) + np.array(J1))
    >>> c[K] == a[I]*b[J]
    True

    """
    b = asanyarray(b)
    a = array(a, copy=False, subok=True, ndmin=b.ndim)
    ndb, nda = b.ndim, a.ndim
    if (nda == 0 or ndb == 0):
        return _nx.multiply(a, b)
    as_ = a.shape
    bs = b.shape
    if not a.flags.contiguous:
        a = reshape(a, as_)
    if not b.flags.contiguous:
        b = reshape(b, bs)
    nd = ndb
    if (ndb != nda):
        if (ndb > nda):
            as_ = (1,)*(ndb-nda) + as_
        else:
            bs = (1,)*(nda-ndb) + bs
            nd = nda
    result = outer(a, b).reshape(as_+bs)
    axis = nd-1
    for _ in range(nd):
        result = concatenate(result, axis=axis)
    wrapper = get_array_prepare(a, b)
    if wrapper is not None:
        result = wrapper(result)
    wrapper = get_array_wrap(a, b)
    if wrapper is not None:
        result = wrapper(result)
    return result
