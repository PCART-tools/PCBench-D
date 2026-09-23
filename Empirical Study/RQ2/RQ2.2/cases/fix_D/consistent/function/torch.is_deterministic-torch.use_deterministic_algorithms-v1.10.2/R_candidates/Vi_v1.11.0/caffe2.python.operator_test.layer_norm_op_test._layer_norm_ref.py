def _layer_norm_ref(axis, epsilon, X):
    left = int(np.prod(X.shape[:axis]))
    reshaped = np.reshape(X, [left, -1])
    mean = np.mean(reshaped, axis=1).reshape([left, 1])
    std = np.sqrt(np.mean(np.square(reshaped), axis=1).reshape(
        [left, 1]) - np.square(mean) + epsilon)
    Y = (reshaped - mean) / (std)
    Y = np.reshape(Y, X.shape)
    mean = np.reshape(mean, X.shape[:axis] + (1,))
    std = np.reshape(std, X.shape[:axis] + (1,))
    return (Y, mean, std)
