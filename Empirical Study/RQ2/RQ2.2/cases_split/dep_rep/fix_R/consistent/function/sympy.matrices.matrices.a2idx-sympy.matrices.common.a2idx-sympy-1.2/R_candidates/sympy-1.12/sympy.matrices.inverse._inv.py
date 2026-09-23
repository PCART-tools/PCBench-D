def _inv(M, method=None, iszerofunc=_iszero, try_block_diag=False):
    """
    Return the inverse of a matrix using the method indicated. Default for
    dense matrices is is Gauss elimination, default for sparse matrices is LDL.

    Parameters
    ==========

    method : ('GE', 'LU', 'ADJ', 'CH', 'LDL')

    iszerofunc : function, optional
        Zero-testing function to use.

    try_block_diag : bool, optional
        If True then will try to form block diagonal matrices using the
        method get_diag_blocks(), invert these individually, and then
        reconstruct the full inverse matrix.

    Examples
    ========

    >>> from sympy import SparseMatrix, Matrix
    >>> A = SparseMatrix([
    ... [ 2, -1,  0],
    ... [-1,  2, -1],
    ... [ 0,  0,  2]])
    >>> A.inv('CH')
    Matrix([
    [2/3, 1/3, 1/6],
    [1/3, 2/3, 1/3],
    [  0,   0, 1/2]])
    >>> A.inv(method='LDL') # use of 'method=' is optional
    Matrix([
    [2/3, 1/3, 1/6],
    [1/3, 2/3, 1/3],
    [  0,   0, 1/2]])
    >>> A * _
    Matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]])
    >>> A = Matrix(A)
    >>> A.inv('CH')
    Matrix([
    [2/3, 1/3, 1/6],
    [1/3, 2/3, 1/3],
    [  0,   0, 1/2]])
    >>> A.inv('ADJ') == A.inv('GE') == A.inv('LU') == A.inv('CH') == A.inv('LDL') == A.inv('QR')
    True

    Notes
    =====

    According to the ``method`` keyword, it calls the appropriate method:

        GE .... inverse_GE(); default for dense matrices
        LU .... inverse_LU()
        ADJ ... inverse_ADJ()
        CH ... inverse_CH()
        LDL ... inverse_LDL(); default for sparse matrices
        QR ... inverse_QR()

    Note, the GE and LU methods may require the matrix to be simplified
    before it is inverted in order to properly detect zeros during
    pivoting. In difficult cases a custom zero detection function can
    be provided by setting the ``iszerofunc`` argument to a function that
    should return True if its argument is zero. The ADJ routine computes
    the determinant and uses that to detect singular matrices in addition
    to testing for zeros on the diagonal.

    See Also
    ========

    inverse_ADJ
    inverse_GE
    inverse_LU
    inverse_CH
    inverse_LDL

    Raises
    ======

    ValueError
        If the determinant of the matrix is zero.
    """

    from sympy.matrices import diag, SparseMatrix

    if method is None:
        method = 'LDL' if isinstance(M, SparseMatrix) else 'GE'

    if try_block_diag:
        blocks = M.get_diag_blocks()
        r      = []

        for block in blocks:
            r.append(block.inv(method=method, iszerofunc=iszerofunc))

        return diag(*r)

    if method == "GE":
        rv = M.inverse_GE(iszerofunc=iszerofunc)
    elif method == "LU":
        rv = M.inverse_LU(iszerofunc=iszerofunc)
    elif method == "ADJ":
        rv = M.inverse_ADJ(iszerofunc=iszerofunc)
    elif method == "CH":
        rv = M.inverse_CH(iszerofunc=iszerofunc)
    elif method == "LDL":
        rv = M.inverse_LDL(iszerofunc=iszerofunc)
    elif method == "QR":
        rv = M.inverse_QR(iszerofunc=iszerofunc)
    elif method == "BLOCK":
        rv = M.inverse_BLOCK(iszerofunc=iszerofunc)
    else:
        raise ValueError("Inversion method unrecognized")

    return M._new(rv)
