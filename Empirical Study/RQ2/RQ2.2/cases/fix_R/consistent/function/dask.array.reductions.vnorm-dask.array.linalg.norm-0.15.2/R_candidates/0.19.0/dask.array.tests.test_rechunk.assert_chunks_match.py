def assert_chunks_match(left, right):
    for x, y in zip(left, right):
        if np.isnan(x).any():
            assert np.isnan(x).all()
        else:
            assert x == y
