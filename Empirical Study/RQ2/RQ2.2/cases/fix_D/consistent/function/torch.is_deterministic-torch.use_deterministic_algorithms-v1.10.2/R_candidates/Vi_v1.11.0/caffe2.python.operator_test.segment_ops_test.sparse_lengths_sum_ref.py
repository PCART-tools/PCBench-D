def sparse_lengths_sum_ref(D, I, L, normalize_by_lengths=False):
    R = np.zeros(shape=(L.size,) + D.shape[1:], dtype=np.float32)
    line = 0
    for g in range(L.size):
        for _ in range(L[g]):
            if len(D.shape) > 1:
                R[g, :] += D[I[line], :]
            else:
                R[g] += D[I[line]]
            line += 1

        if normalize_by_lengths and L[g] > 1:
            if len(D.shape) > 1:
                R[g, :] = R[g, :] / L[g]
            else:
                R[g] = R[g] / L[g]

    return [R]
