def _remove_redundancy_dense(A, rhs):
    """
    Eliminates redundant equations from system of equations defined by Ax = b
    and identifies infeasibilities.

    Parameters
    ----------
    A : 2-D sparse matrix
        An matrix representing the left-hand side of a system of equations
    rhs : 1-D array
        An array representing the right-hand side of a system of equations

    Returns
    ----------
    A : 2-D sparse matrix
        A matrix representing the left-hand side of a system of equations
    rhs : 1-D array
        An array representing the right-hand side of a system of equations
    status: int
        An integer indicating the status of the system
        0: No infeasibility identified
        2: Trivially infeasible
    message : str
        A string descriptor of the exit status of the optimization.

    References
    ----------
    .. [2] Andersen, Erling D. "Finding all linearly dependent rows in
           large-scale linear programming." Optimization Methods and Software
           6.3 (1995): 219-227.

    """
    tolapiv = 1e-8
    tolprimal = 1e-8
    status = 0
    message = ""
    inconsistent = ("There is a linear combination of rows of A_eq that "
                    "results in zero, suggesting a redundant constraint. "
                    "However the same linear combination of b_eq is "
                    "nonzero, suggesting that the constraints conflict "
                    "and the problem is infeasible.")
    A, rhs, status, message = _remove_zero_rows(A, rhs)

    if status != 0:
        return A, rhs, status, message

    m, n = A.shape

    v = list(range(m))      # Artificial column indices.
    b = list(v)             # Basis column indices.
    # This is better as a list than a set because column order of basis matrix
    # needs to be consistent.
    k = set(range(m, m+n))  # Structural column indices.
    d = []                  # Indices of dependent rows
    lu = None
    perm_r = None

    A_orig = A
    A = np.hstack((np.eye(m), A))
    e = np.zeros(m)

    # Implements basic algorithm from [2]
    # Uses some of the suggested improvements (removing zero rows and
    # Bartels-Golub update idea).
    # Removing column singletons would be easy, but it is not as important
    # because the procedure is performed only on the equality constraint
    # matrix from the original problem - not on the canonical form matrix,
    # which would have many more column singletons due to slack variables
    # from the inequality constraints.
    # The thoughts on "crashing" the initial basis sound useful, but the
    # description of the procedure seems to assume a lot of familiarity with
    # the subject; it is not very explicit. I already went through enough
    # trouble getting the basic algorithm working, so I was not interested in
    # trying to decipher this, too. (Overall, the paper is fraught with
    # mistakes and ambiguities - which is strange, because the rest of
    # Andersen's papers are quite good.)

    B = A[:, b]
    for i in v:

        e[i] = 1
        if i > 0:
            e[i-1] = 0

        try:  # fails for i==0 and any time it gets ill-conditioned
            j = b[i-1]
            lu = bg_update_dense(lu, perm_r, A[:, j], i-1)
        except:
            lu = scipy.linalg.lu_factor(B)
            LU, p = lu
            perm_r = list(range(m))
            for i1, i2 in enumerate(p):
                perm_r[i1], perm_r[i2] = perm_r[i2], perm_r[i1]

        pi = scipy.linalg.lu_solve(lu, e, trans=1)

        # not efficient, but this is not the time sink...
        js = np.array(list(k-set(b)))
        batch = 50
        dependent = True

        # This is a tiny bit faster than looping over columns indivually,
        # like for j in js: if abs(A[:,j].transpose().dot(pi)) > tolapiv:
        for j_index in range(0, len(js), batch):
            j_indices = js[np.arange(j_index, min(j_index+batch, len(js)))]

            c = abs(A[:, j_indices].transpose().dot(pi))
            if (c > tolapiv).any():
                j = js[j_index + np.argmax(c)]  # very independent column
                B[:, i] = A[:, j]
                b[i] = j
                dependent = False
                break
        if dependent:
            bibar = pi.T.dot(rhs.reshape(-1, 1))
            bnorm = np.linalg.norm(rhs)
            if abs(bibar)/(1+bnorm) > tolprimal:  # inconsistent
                status = 2
                message = inconsistent
                return A_orig, rhs, status, message
            else:  # dependent
                d.append(i)

    keep = set(range(m))
    keep = list(keep - set(d))
    return A_orig[keep, :], rhs[keep], status, message
