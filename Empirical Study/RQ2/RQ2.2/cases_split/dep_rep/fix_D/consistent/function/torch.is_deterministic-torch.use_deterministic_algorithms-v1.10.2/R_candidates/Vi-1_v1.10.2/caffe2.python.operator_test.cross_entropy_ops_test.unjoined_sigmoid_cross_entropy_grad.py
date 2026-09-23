def unjoined_sigmoid_cross_entropy_grad(x, z):
    return z - (1. - z) / (1. + np.exp(-x))
