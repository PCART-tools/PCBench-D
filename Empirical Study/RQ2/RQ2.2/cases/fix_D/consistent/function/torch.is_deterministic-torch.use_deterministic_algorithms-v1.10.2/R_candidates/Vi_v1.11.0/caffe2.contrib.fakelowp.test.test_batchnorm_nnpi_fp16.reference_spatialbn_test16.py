def reference_spatialbn_test16(X, scale, bias, mean, var, epsilon, order):
    X = X.astype(np.float16)
    scale = scale.astype(np.float16)
    bias = bias.astype(np.float16)
    mean = mean.astype(np.float16)
    # var = var.astype(np.float16)
    assert(order == "NCHW")

    scale = scale[np.newaxis, :, np.newaxis, np.newaxis]
    bias = bias[np.newaxis, :, np.newaxis, np.newaxis]
    mean = mean[np.newaxis, :, np.newaxis, np.newaxis]
    var = var[np.newaxis, :, np.newaxis, np.newaxis]
    Y = ((X - mean) * (scale / np.sqrt(var + epsilon).astype(np.float16))) + bias
    return Y.astype(np.float32)
