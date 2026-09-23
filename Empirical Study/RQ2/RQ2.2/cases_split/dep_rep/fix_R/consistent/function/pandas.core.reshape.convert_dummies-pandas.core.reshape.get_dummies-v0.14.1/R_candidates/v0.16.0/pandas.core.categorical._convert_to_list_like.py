def _convert_to_list_like(list_like):
    if hasattr(list_like, "dtype"):
        return list_like
    if isinstance(list_like, list):
        return list_like
    if (is_sequence(list_like) or isinstance(list_like, tuple)
        or isinstance(list_like, types.GeneratorType)):
        return list(list_like)
    elif np.isscalar(list_like):
        return [list_like]
    else:
        # is this reached?
        return [list_like]
