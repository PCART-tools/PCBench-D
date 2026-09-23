def _get_random_tensor_and_q_params(shapes, rand_scale, torch_type):
    X = (torch.rand(*shapes, dtype=torch.float) - 0.5) * rand_scale
    # Calculate reasonable quantization params
    min_val = torch.min(X)
    max_val = torch.max(X)
    if torch_type == torch.qint32:
        X_zero_point = int(torch.randint(-1 * (2 ** 31), 2 ** 31 - 1, (1,)))
        num_bins = 2 ** 32
        X_scale = float(max_val - min_val) / num_bins
    elif torch_type == torch.qint8:
        X_zero_point = int(torch.randint(-128, 127, (1,)))
        num_bins = 2 ** 8
        X_scale = float(max_val - min_val) / num_bins
    else:  # torch.quint8
        X_zero_point = 127
        num_bins = 2 ** 8
        X_scale = float(max_val - min_val) / num_bins
    if X_scale == 0:
        X_scale = 1e-10
    return X, X_scale, X_zero_point
