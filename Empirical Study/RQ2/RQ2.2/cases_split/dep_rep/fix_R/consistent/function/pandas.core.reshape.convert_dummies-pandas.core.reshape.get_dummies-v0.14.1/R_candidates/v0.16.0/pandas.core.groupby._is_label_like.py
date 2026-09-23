def _is_label_like(val):
    return isinstance(val, compat.string_types) or np.isscalar(val)
