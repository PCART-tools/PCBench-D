@np.vectorize
@lru_cache(maxsize=128)
def _comb(n, k):
    if k > n:
        return 0
    k = min(k, n - k)
    i = np.arange(1, k + 1)
    return np.prod((n + 1 - i)/i).astype(int)
