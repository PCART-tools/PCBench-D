def _proj_transform_vec_clip(vec, M):
    vecw = np.dot(M, vec)
    w = vecw[3]
    # clip here.
    txs, tys, tzs = vecw[0] / w, vecw[1] / w, vecw[2] / w
    tis = (0 <= vecw[0]) & (vecw[0] <= 1) & (0 <= vecw[1]) & (vecw[1] <= 1)
    if np.any(tis):
        tis = vecw[1] < 1
    return txs, tys, tzs, tis
