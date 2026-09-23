@wraps(np.extract)
def extract(condition, arr):
    if not isinstance(condition, Array):
        condition = np.array(condition, dtype=bool)
    return compress(condition.ravel(), arr.ravel())
