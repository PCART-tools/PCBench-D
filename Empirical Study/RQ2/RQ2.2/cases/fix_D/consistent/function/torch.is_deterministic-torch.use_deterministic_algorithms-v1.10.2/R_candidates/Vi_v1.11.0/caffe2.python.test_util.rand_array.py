def rand_array(*dims):
    # np.random.rand() returns float instead of 0-dim array, that's why need to
    # do some tricks
    return np.array(np.random.rand(*dims) - 0.5).astype(np.float32)
