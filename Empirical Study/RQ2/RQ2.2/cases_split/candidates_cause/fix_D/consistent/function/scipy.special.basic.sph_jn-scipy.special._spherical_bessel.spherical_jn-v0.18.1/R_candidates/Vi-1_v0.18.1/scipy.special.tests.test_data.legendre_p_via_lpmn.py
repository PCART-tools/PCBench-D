def legendre_p_via_lpmn(n, x):
    return lpmn(0, n, x)[0][0,-1]
