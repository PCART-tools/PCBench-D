def jac_complex_sparse(t, y):
    return csc_matrix(jac_complex(t, y))
