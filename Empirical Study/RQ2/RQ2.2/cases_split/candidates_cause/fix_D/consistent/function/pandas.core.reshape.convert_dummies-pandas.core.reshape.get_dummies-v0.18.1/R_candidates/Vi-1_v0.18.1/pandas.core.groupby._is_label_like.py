def _is_label_like(val):
    return (isinstance(val, compat.string_types) or
            (val is not None and lib.isscalar(val)))
