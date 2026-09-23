def sigmoid_cross_entropy_with_logits(x, z):
    return np.maximum(x, 0) - x * z + np.log(1 + np.exp(-np.abs(x)))
