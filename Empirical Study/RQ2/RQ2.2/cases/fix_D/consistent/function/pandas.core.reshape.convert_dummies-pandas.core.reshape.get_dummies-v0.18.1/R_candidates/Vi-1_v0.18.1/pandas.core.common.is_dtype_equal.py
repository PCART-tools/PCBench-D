def is_dtype_equal(source, target):
    """ return a boolean if the dtypes are equal """
    try:
        source = _get_dtype(source)
        target = _get_dtype(target)
        return source == target
    except (TypeError, AttributeError):

        # invalid comparison
        # object == category will hit this
        return False
