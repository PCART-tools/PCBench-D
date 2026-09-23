def _maybe_convert_string_to_object(values):
    """
    Convert string-like and string-like array to convert object dtype.
    This is to avoid numpy to handle the array as str dtype.
    """
    if isinstance(values, string_types):
        values = np.array([values], dtype=object)
    elif (isinstance(values, np.ndarray) and
        issubclass(values.dtype.type, (np.string_, np.unicode_))):
        values = values.astype(object)
    return values
