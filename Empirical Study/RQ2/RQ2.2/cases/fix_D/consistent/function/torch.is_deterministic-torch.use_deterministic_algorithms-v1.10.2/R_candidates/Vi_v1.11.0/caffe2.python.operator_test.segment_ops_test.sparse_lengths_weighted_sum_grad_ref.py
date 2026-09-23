def sparse_lengths_weighted_sum_grad_ref(
        GO, fwd_out, fwd_in, grad_on_weights=False):
    D, W, I, L = fwd_in
    GI = np.zeros(shape=(len(I), ) + D.shape[1:], dtype=D.dtype)
    GW = np.zeros(shape=W.shape, dtype=W.dtype) if grad_on_weights else None
    line = 0
    for g in range(len(L)):
        for _ in range(L[g]):
            if len(GO.shape) > 1:
                GI[line, :] = W[line] * GO[g, :]
            else:
                GI[line] = W[line] * GO[g]
            if GW is not None:
                if len(GO.shape) > 1:
                    GW[line] = np.dot(GO[g].flatten(), D[I[line], :].flatten())
                else:
                    GW[line] = np.dot(GO[g].flatten(), D[I[line]].flatten())
            line += 1
    print(GW)
    return [(GI, I), GW, None, None]
