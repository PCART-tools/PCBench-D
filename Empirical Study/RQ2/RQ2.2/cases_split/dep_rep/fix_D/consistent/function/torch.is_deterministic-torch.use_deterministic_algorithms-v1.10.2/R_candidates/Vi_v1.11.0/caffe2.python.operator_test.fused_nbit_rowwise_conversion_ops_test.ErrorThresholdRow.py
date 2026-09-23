def ErrorThresholdRow(X, bit_rate):
    # minimum representable error in bit_rate per row
    min_elem = np.min(X, axis=1)
    max_elem = np.max(X, axis=1)

    bias = np.float16(min_elem)
    scale = np.float16((max_elem - bias) / ((1 << bit_rate) - 1))

    max_round_error = scale / 2
    max_clip_error = np.maximum(
        np.abs(min_elem - bias), np.abs(scale * ((1 << bit_rate) - 1) + bias - max_elem)
    )
    thres = np.maximum(max_round_error, max_clip_error) * 1.1
    return thres
