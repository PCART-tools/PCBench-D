def maybe_convert_platform(values):
    """ try to do platform conversion, allow ndarray or list here """

    if isinstance(values, (list, tuple, range)):
        values = construct_1d_object_array_from_listlike(values)
    if getattr(values, "dtype", None) == np.object_:
        if hasattr(values, "_values"):
            values = values._values
        values = lib.maybe_convert_objects(values)

    return values
