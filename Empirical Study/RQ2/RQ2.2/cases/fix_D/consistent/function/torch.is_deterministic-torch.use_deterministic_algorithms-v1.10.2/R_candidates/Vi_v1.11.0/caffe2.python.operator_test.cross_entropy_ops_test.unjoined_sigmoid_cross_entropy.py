def unjoined_sigmoid_cross_entropy(x, z):
    return -z * x + (1. - z) * np.maximum(x, 0) \
        + (1. - z) * np.log(1 + np.exp(-np.abs(x)))
