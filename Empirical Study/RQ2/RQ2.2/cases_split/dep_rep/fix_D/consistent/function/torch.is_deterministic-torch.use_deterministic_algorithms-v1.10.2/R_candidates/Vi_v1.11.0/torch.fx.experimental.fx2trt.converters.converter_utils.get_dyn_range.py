def get_dyn_range(scale, zero_point, dtype):
    """
    Get the dynamic range of a tensor based on its scale, zero_point and dtype.
    """
    if dtype == torch.quint8:
        min_val, max_val = 0, 255
    elif dtype == torch.qint8:
        min_val, max_val = -128, 127
    else:
        raise RuntimeError(f"Unsupported quantized dtype {dtype}")

    return (min_val - zero_point) * scale, (max_val - zero_point) * scale
