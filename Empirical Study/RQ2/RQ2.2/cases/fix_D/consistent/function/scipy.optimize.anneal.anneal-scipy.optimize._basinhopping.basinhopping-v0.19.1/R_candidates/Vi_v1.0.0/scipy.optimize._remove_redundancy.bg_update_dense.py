def bg_update_dense(plu, perm_r, v, j):
    LU, p = plu

    u = scipy.linalg.solve_triangular(LU, v[perm_r], lower=True,
                                      unit_diagonal=True)
    LU[:j+1, j] = u[:j+1]
    l = u[j+1:]
    piv = LU[j, j]
    LU[j+1:, j] += (l/piv)
    return LU, p
