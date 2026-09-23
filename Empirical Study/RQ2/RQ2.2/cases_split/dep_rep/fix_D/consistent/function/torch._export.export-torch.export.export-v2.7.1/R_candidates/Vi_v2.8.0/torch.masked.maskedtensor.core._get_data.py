def _get_data(a):
    if is_masked_tensor(a):
        return a._masked_data
    return a
