def _dense_difference(fun, x0, f0, h, use_one_sided, method):
    m = f0.size
    n = x0.size
    J_transposed = np.empty((n, m))
    h_vecs = np.diag(h)

    for i in range(h.size):
        if method == '2-point':
            x = x0 + h_vecs[i]
            dx = x[i] - x0[i]  # Recompute dx as exactly representable number.
            df = fun(x) - f0
        elif method == '3-point' and use_one_sided[i]:
            x1 = x0 + h_vecs[i]
            x2 = x0 + 2 * h_vecs[i]
            dx = x2[i] - x0[i]
            f1 = fun(x1)
            f2 = fun(x2)
            df = -3.0 * f0 + 4 * f1 - f2
        elif method == '3-point' and not use_one_sided[i]:
            x1 = x0 - h_vecs[i]
            x2 = x0 + h_vecs[i]
            dx = x2[i] - x1[i]
            f1 = fun(x1)
            f2 = fun(x2)
            df = f2 - f1
        elif method == 'cs':
            f1 = fun(x0 + h_vecs[i]*1.j)
            df = f1.imag
            dx = h_vecs[i, i]
        else:
            raise RuntimeError("Never be here.")

        J_transposed[i] = df / dx

    if m == 1:
        J_transposed = np.ravel(J_transposed)

    return J_transposed.T
