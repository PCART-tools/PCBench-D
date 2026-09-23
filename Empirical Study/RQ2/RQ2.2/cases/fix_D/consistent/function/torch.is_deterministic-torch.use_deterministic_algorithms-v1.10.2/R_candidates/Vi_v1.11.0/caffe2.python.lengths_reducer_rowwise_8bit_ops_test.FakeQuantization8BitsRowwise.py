def FakeQuantization8BitsRowwise(data):
    min_el = np.min(data, axis=1)
    max_el = np.max(data, axis=1)
    scale = (max_el - min_el) / 255.
    bias = min_el
    inv_scale = 1. / scale
    data = data.T
    data = np.round((data - bias) * inv_scale) * scale + bias
    return data.T
