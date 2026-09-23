def is_numpy_type_info(obj) -> bool:
    if np is None:
        return False
    return isinstance(obj, (np.finfo, np.iinfo))
