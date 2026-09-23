def _proj_transform_vec(vec, M):
    vecw = np.dot(M, vec)
    w = vecw[3]
    # clip here..
    txs, tys, tzs = vecw[0]/w, vecw[1]/w, vecw[2]/w
    return txs, tys, tzs
