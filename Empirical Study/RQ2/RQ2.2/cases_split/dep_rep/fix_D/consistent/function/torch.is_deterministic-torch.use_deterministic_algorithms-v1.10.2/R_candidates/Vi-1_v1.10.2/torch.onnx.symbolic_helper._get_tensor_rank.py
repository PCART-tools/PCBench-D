def _get_tensor_rank(x):
    if not _is_tensor(x) or x.type() is None:
        return None
    return x.type().dim()
