def _layer_norm_grad_ref(axis, gout_full, norm, mean_full, stdev_full, X_full):
    left = int(np.prod(X_full.shape[:axis]))
    right = int(np.prod(X_full.shape[axis:]))
    X = np.reshape(X_full, [left, right])
    stdev = np.reshape(stdev_full, [left, 1])
    mean = np.reshape(mean_full, [left, 1])
    gout = np.reshape(gout_full, [left, right])
    dstdev_end = (-1.0) / np.power(stdev, 2.0) \
        * np.sum((X - mean) * gout, axis=1).reshape([left, 1])
    dmean_end = np.sum(-1.0 / stdev * gout, axis=1).reshape([left, 1])
    dx_end = 1.0 / stdev * gout

    # stdev block
    dmean_stdev = -1.0 * mean / stdev * dstdev_end
    dx_stdev = X / (right * stdev) * dstdev_end

    # mean block
    dmean = dmean_end + dmean_stdev
    dxmean = (1.0 / right) * dmean

    # final outputs
    dx = dx_end + dx_stdev + dxmean
    dx = dx.reshape(X_full.shape)

    return [dx]
