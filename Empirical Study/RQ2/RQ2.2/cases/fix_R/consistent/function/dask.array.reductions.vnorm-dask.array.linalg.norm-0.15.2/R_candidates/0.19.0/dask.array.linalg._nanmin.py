def _nanmin(m, n):
    k_0 = min([m, n])
    k_1 = m if np.isnan(n) else n
    return k_1 if np.isnan(k_0) else k_0
