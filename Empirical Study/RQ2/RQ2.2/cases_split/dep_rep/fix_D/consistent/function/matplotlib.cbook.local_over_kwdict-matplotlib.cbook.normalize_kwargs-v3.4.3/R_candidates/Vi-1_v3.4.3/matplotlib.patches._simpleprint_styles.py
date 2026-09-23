def _simpleprint_styles(_styles):
    """
    A helper function for the _Style class.  Given the dictionary of
    {stylename: styleclass}, return a string rep of the list of keys.
    Used to update the documentation.
    """
    return "[{}]".format("|".join(map(" '{}' ".format, sorted(_styles))))
