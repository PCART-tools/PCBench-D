def _get_tensor_dim_size(x, dim):
    try:
        sizes = _get_tensor_sizes(x)
        return sizes[dim]
    except Exception:
        pass
    return None
