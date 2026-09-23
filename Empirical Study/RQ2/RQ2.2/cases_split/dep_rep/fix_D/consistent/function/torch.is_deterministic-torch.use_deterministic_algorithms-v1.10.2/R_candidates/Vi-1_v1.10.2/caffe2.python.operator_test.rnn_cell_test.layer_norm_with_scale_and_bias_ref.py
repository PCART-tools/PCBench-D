def layer_norm_with_scale_and_bias_ref(X, scale, bias, axis=-1, epsilon=1e-4):
    left = np.prod(X.shape[:axis])
    reshaped = np.reshape(X, [left, -1])
    mean = np.mean(reshaped, axis=1).reshape([left, 1])
    stdev = np.sqrt(
        np.mean(np.square(reshaped), axis=1).reshape([left, 1]) -
        np.square(mean) + epsilon
    )
    norm = (reshaped - mean) / stdev
    norm = np.reshape(norm, X.shape)
    adjusted = scale * norm + bias

    return adjusted
