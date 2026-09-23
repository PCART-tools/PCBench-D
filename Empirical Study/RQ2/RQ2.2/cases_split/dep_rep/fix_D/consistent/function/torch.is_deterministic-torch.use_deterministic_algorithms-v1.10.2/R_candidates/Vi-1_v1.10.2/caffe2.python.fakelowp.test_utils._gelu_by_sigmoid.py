def _gelu_by_sigmoid(x):
    return np.float64(x) / (1. + np.exp(np.float64(x) * 1.702))
