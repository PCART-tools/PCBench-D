def _minmax_scale_zeropoint(min_val, max_val, qmin=-127, qmax=128, eps=torch.finfo(torch.float32).eps):
    min_val = min(0.0, min_val)
    max_val = max(0.0, max_val)
    if max_val == min_val:
        return 1.0, 0
    else:
        scale = (max_val - min_val) / float(qmax - qmin)
        scale = max(scale, eps)
        zero_point = qmin - round(min_val / scale)
        zero_point = max(qmin, zero_point)
        zero_point = min(qmax, zero_point)
        zero_point = int(zero_point)
        return scale, zero_point
