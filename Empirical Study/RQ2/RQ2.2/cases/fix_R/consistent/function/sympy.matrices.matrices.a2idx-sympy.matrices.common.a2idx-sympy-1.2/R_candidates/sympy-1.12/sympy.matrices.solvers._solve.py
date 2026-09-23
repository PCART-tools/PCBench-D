def _solve(M, rhs, method='GJ'):
    """Solves linear equation where the unique solution exists.

    Parameters
    ==========

    rhs : Matrix
        Vector representing the right hand side of the linear equation.

    method : string, optional
        If set to ``'GJ'`` or ``'GE'``, the Gauss-Jordan elimination will be
        used, which is implemented in the routine ``gauss_jordan_solve``.

        If set to ``'LU'``, ``LUsolve`` routine will be used.

        If set to ``'QR'``, ``QRsolve`` routine will be used.

        If set to ``'PINV'``, ``pinv_solve`` routine will be used.

        It also supports the methods available for special linear systems

        For positive definite systems:

        If set to ``'CH'``, ``cholesky_solve`` routine will be used.

        If set to ``'LDL'``, ``LDLsolve`` routine will be used.

        To use a different method and to compute the solution via the
        inverse, use a method defined in the .inv() docstring.

    Returns
    =======

    solutions : Matrix
        Vector representing the solution.

    Raises
    ======

    ValueError
        If there is not a unique solution then a ``ValueError`` will be
        raised.

        If ``M`` is not square, a ``ValueError`` and a different routine
        for solving the system will be suggested.
    """

    if method in ('GJ', 'GE'):
        try:
            soln, param = M.gauss_jordan_solve(rhs)

            if param:
                raise NonInvertibleMatrixError("Matrix det == 0; not invertible. "
                "Try ``M.gauss_jordan_solve(rhs)`` to obtain a parametric solution.")

        except ValueError:
            raise NonInvertibleMatrixError("Matrix det == 0; not invertible.")

        return soln

    elif method == 'LU':
        return M.LUsolve(rhs)
    elif method == 'CH':
        return M.cholesky_solve(rhs)
    elif method == 'QR':
        return M.QRsolve(rhs)
    elif method == 'LDL':
        return M.LDLsolve(rhs)
    elif method == 'PINV':
        return M.pinv_solve(rhs)
    else:
        return M.inv(method=method).multiply(rhs)
