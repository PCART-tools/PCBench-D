def random_entry(n, min_eig, max_eig, case):

    # Generate random matrix
    rand = np.random.uniform(-1, 1, (n, n))

    # QR decomposition
    Q, _, _ = qr(rand, pivoting='True')

    # Generate random eigenvalues
    eigvalues = np.random.uniform(min_eig, max_eig, n)
    eigvalues = np.sort(eigvalues)[::-1]

    # Generate matrix
    Qaux = np.multiply(eigvalues, Q)
    A = np.dot(Qaux, Q.T)

    # Generate gradient vector accordingly
    # to the case is being tested.
    if case == 'hard':
        g = np.zeros(n)
        g[:-1] = np.random.uniform(-1, 1, n-1)
        g = np.dot(Q, g)
    elif case == 'jac_equal_zero':
        g = np.zeros(n)
    else:
        g = np.random.uniform(-1, 1, n)

    return A, g
