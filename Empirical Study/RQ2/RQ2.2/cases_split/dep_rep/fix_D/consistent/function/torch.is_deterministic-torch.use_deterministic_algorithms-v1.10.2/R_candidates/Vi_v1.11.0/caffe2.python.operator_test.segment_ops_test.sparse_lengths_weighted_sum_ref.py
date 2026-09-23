def sparse_lengths_weighted_sum_ref(D, W, I, L):
    R = np.zeros(shape=(len(L), ) + D.shape[1:], dtype=D.dtype)
    line = 0
    for g in range(len(L)):
        for _ in range(L[g]):
            if len(D.shape) > 1:
                R[g, :] += W[line] * D[I[line], :]
            else:
                R[g] += W[line] * D[I[line]]
            line += 1
    return [R]
