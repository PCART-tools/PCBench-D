def ensure_dtype_can_hold_na(dtype: DtypeObj) -> DtypeObj:
    """
    If we have a dtype that cannot hold NA values, find the best match that can.
    """
    if isinstance(dtype, ExtensionDtype):
        # TODO: ExtensionDtype.can_hold_na?
        return dtype
    elif dtype.kind == "b":
        return np.dtype(object)
    elif dtype.kind in ["i", "u"]:
        return np.dtype(np.float64)
    return dtype
