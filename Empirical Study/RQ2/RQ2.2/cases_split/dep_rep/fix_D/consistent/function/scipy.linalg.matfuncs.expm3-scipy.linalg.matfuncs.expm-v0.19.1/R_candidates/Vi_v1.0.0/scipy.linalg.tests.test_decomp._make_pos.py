def _make_pos(X):
    # the decompositions can have different signs than verified results
    return np.sign(X)*X
