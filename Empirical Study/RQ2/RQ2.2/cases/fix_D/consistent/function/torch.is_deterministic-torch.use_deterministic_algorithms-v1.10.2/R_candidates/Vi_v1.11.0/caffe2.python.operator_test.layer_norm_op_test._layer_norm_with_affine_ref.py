def _layer_norm_with_affine_ref(axis, epsilon, X, gamma, beta):
    Y, mean, std = _layer_norm_ref(axis, epsilon, X)
    Y = Y * gamma + beta
    return (Y, mean, std)
