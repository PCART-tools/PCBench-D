def _sparse_difference(fun, x0, f0, h, use_one_sided,
                       structure, groups, method):
    m = f0.size
    n = x0.size
    row_indices = []
    col_indices = []
    fractions = []

    n_groups = np.max(groups) + 1
    for group in range(n_groups):
        # Perturb variables which are in the same group simultaneously.
        e = np.equal(group, groups)
        h_vec = h * e
        if method == '2-point':
            x = x0 + h_vec
            dx = x - x0
            df = fun(x) - f0
            # The result is  written to columns which correspond to perturbed
            # variables.
            cols, = np.nonzero(e)
            # Find all non-zero elements in selected columns of Jacobian.
            i, j, _ = find(structure[:, cols])
            # Restore column indices in the full array.
            j = cols[j]
        elif method == '3-point':
            # Here we do conceptually the same but separate one-sided
            # and two-sided schemes.
            x1 = x0.copy()
            x2 = x0.copy()

            mask_1 = use_one_sided & e
            x1[mask_1] += h_vec[mask_1]
            x2[mask_1] += 2 * h_vec[mask_1]

            mask_2 = ~use_one_sided & e
            x1[mask_2] -= h_vec[mask_2]
            x2[mask_2] += h_vec[mask_2]

            dx = np.zeros(n)
            dx[mask_1] = x2[mask_1] - x0[mask_1]
            dx[mask_2] = x2[mask_2] - x1[mask_2]

            f1 = fun(x1)
            f2 = fun(x2)

            cols, = np.nonzero(e)
            i, j, _ = find(structure[:, cols])
            j = cols[j]

            mask = use_one_sided[j]
            df = np.empty(m)

            rows = i[mask]
            df[rows] = -3 * f0[rows] + 4 * f1[rows] - f2[rows]

            rows = i[~mask]
            df[rows] = f2[rows] - f1[rows]
        elif method == 'cs':
            f1 = fun(x0 + h_vec*1.j)
            df = f1.imag
            dx = h_vec
            cols, = np.nonzero(e)
            i, j, _ = find(structure[:, cols])
            j = cols[j]
        else:
            raise ValueError("Never be here.")

        # All that's left is to compute the fraction. We store i, j and
        # fractions as separate arrays and later construct coo_matrix.
        row_indices.append(i)
        col_indices.append(j)
        fractions.append(df[i] / dx[j])

    row_indices = np.hstack(row_indices)
    col_indices = np.hstack(col_indices)
    fractions = np.hstack(fractions)
    J = coo_matrix((fractions, (row_indices, col_indices)), shape=(m, n))
    return csr_matrix(J)
