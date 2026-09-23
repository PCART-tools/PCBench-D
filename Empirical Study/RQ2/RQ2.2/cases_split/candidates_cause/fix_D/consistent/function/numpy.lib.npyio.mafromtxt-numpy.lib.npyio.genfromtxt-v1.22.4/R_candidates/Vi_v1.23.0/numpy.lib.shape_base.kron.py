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
    # Working:
    # 1. Equalise the shapes by prepending smaller array with 1s
    # 2. Expand shapes of both the arrays by adding new axes at
    #    odd positions for 1st array and even positions for 2nd
    # 3. Compute the product of the modified array
    # 4. The inner most array elements now contain the rows of
    #    the Kronecker product
    # 5. Reshape the result to kron's shape, which is same as
    #    product of shapes of the two arrays.
    b = asanyarray(b)
    a = array(a, copy=False, subok=True, ndmin=b.ndim)
    is_any_mat = isinstance(a, matrix) or isinstance(b, matrix)
    ndb, nda = b.ndim, a.ndim
    nd = max(ndb, nda)

    if (nda == 0 or ndb == 0):
        return _nx.multiply(a, b)

    as_ = a.shape
    bs = b.shape
    if not a.flags.contiguous:
        a = reshape(a, as_)
    if not b.flags.contiguous:
        b = reshape(b, bs)

    # Equalise the shapes by prepending smaller one with 1s
    as_ = (1,)*max(0, ndb-nda) + as_
    bs = (1,)*max(0, nda-ndb) + bs

    # Insert empty dimensions
    a_arr = expand_dims(a, axis=tuple(range(ndb-nda)))
    b_arr = expand_dims(b, axis=tuple(range(nda-ndb)))

    # Compute the product
    a_arr = expand_dims(a_arr, axis=tuple(range(1, nd*2, 2)))
    b_arr = expand_dims(b_arr, axis=tuple(range(0, nd*2, 2)))
    # In case of `mat`, convert result to `array`
    result = _nx.multiply(a_arr, b_arr, subok=(not is_any_mat))

    # Reshape back
    result = result.reshape(_nx.multiply(as_, bs))

    return result if not is_any_mat else matrix(result, copy=False)
