@wraps(np.digitize)
def digitize(a, bins, right=False):
    bins = np.asarray(bins)
    dtype = np.digitize([0], bins, right=False).dtype
    return a.map_blocks(np.digitize, dtype=dtype, bins=bins, right=right)
