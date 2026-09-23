def magic_square(n):
    np.random.seed(0)
    M = n * (n**2 + 1) / 2

    numbers = np.arange(n**4) // n**2 + 1

    numbers = numbers.reshape(n**2, n, n)

    zeros = np.zeros((n**2, n, n))

    A_list = []
    b_list = []

    # Rule 1: use every number exactly once
    for i in range(n**2):
        A_row = zeros.copy()
        A_row[i, :, :] = 1
        A_list.append(A_row.flatten())
        b_list.append(1)

    # Rule 2: Only one number per square
    for i in range(n):
        for j in range(n):
            A_row = zeros.copy()
            A_row[:, i, j] = 1
            A_list.append(A_row.flatten())
            b_list.append(1)

    # Rule 3: sum of rows is M
    for i in range(n):
        A_row = zeros.copy()
        A_row[:, i, :] = numbers[:, i, :]
        A_list.append(A_row.flatten())
        b_list.append(M)

    # Rule 4: sum of columns is M
    for i in range(n):
        A_row = zeros.copy()
        A_row[:, :, i] = numbers[:, :, i]
        A_list.append(A_row.flatten())
        b_list.append(M)

    # Rule 5: sum of diagonals is M
    A_row = zeros.copy()
    A_row[:, range(n), range(n)] = numbers[:, range(n), range(n)]
    A_list.append(A_row.flatten())
    b_list.append(M)
    A_row = zeros.copy()
    A_row[:, range(n), range(-1, -n - 1, -1)] = \
        numbers[:, range(n), range(-1, -n - 1, -1)]
    A_list.append(A_row.flatten())
    b_list.append(M)

    A = np.array(np.vstack(A_list), dtype=float)
    b = np.array(b_list, dtype=float)
    c = np.random.rand(A.shape[1])

    return A, b, c, numbers
