def clarkson_woodruff_transform(input_matrix, sketch_size, seed=None):
    r""""
    Find low-rank matrix approximation via the Clarkson-Woodruff Transform.

    Given an input_matrix ``A`` of size ``(n, d)``, compute a matrix ``A'`` of
    size (sketch_size, d) which holds:

    .. math:: ||Ax|| = (1 \pm \epsilon)||A'x||

    with high probability.

    The error is related to the number of rows of the sketch and it is bounded

    .. math:: poly(r(\epsilon^{-1}))

    Parameters
    ----------
    input_matrix: array_like
        Input matrix, of shape ``(n, d)``.
    sketch_size: int
        Number of rows for the sketch.
    seed : None or int or `numpy.random.RandomState` instance, optional
        This parameter defines the ``RandomState`` object to use for drawing
        random variates.
        If None (or ``np.random``), the global ``np.random`` state is used.
        If integer, it is used to seed the local ``RandomState`` instance.
        Default is None.

    Returns
    -------
    A' : array_like
        Sketch of the input matrix ``A``, of size ``(sketch_size, d)``.

    Notes
    -----
    This is an implementation of the Clarkson-Woodruff Transform (CountSketch).
    ``A'`` can be computed in principle in ``O(nnz(A))`` (with ``nnz`` meaning
    the number of nonzero entries), however we don't take advantage of sparse
    matrices in this implementation.

    Examples
    --------
    Given a big dense matrix ``A``:

    >>> from scipy import linalg
    >>> n_rows, n_columns, sketch_n_rows = (2000, 100, 100)
    >>> threshold = 0.1
    >>> tmp = np.random.normal(0, 0.1, n_rows*n_columns)
    >>> A = np.reshape(tmp, (n_rows, n_columns))
    >>> sketch = linalg.clarkson_woodruff_transform(A, sketch_n_rows)
    >>> sketch.shape
    (100, 100)
    >>> normA = linalg.norm(A)
    >>> norm_sketch = linalg.norm(sketch)

    Now with high probability, the condition ``abs(normA-normSketch) <
    threshold`` holds.

    References
    ----------
    .. [1] Kenneth L. Clarkson and David P. Woodruff. Low rank approximation and
           regression in input sparsity time. In STOC, 2013.

    """
    S = cwt_matrix(sketch_size, input_matrix.shape[0], seed)
    return np.dot(S, input_matrix)
