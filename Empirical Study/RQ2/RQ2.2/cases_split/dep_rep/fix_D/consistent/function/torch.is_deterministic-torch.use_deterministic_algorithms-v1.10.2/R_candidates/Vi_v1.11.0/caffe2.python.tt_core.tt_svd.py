def tt_svd(W, sizes, tt_ranks):
    """
    Helper method for the matrix_to_tt() method performing the TT-SVD
    decomposition.

    Uses the TT-decomposition algorithm to convert a matrix to TT-format using
    multiple reduced SVD operations.

    Args:
        W: two-dimensional weight matrix representing a fully connected layer to
           be converted to TT-format preprocessed by the matrix_to_tt() method.
        sizes: list of the dimensions of each of the cores
        tt_ranks: list of the ranks of the respective cores

    Returns:
        cores: One-dimensional list of cores concatentated along an axis
   """

    assert(len(tt_ranks) == len(sizes) + 1)

    C = W.copy()
    total_size = sizes.size
    core = np.zeros(np.sum(tt_ranks[:-1] * sizes * tt_ranks[1:]),
                    dtype='float32')

    # Compute iterative reduced SVD operations and store each resulting U matrix
    # as an individual core.
    pos = 0
    for i in range(0, total_size - 1):
        shape = tt_ranks[i] * sizes[i]
        C = np.reshape(C, [shape, -1])
        U, S, V = np.linalg.svd(C, full_matrices=False)
        U = U[:, 0:tt_ranks[i + 1]]
        S = S[0:tt_ranks[i + 1]]
        V = V[0:tt_ranks[i + 1], :]

        core[pos:pos + tt_ranks[i] * sizes[i] * tt_ranks[i + 1]] = U.ravel()
        pos += tt_ranks[i] * sizes[i] * tt_ranks[i + 1]
        C = np.dot(np.diag(S), V)

    core[pos:pos + tt_ranks[total_size - 1] *
         sizes[total_size - 1] * tt_ranks[total_size]] = C.ravel()
    return core
