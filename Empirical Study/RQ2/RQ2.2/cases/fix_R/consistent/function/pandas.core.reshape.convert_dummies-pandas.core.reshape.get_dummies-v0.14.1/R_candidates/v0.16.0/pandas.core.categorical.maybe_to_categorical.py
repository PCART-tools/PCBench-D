def maybe_to_categorical(array):
    """ coerce to a categorical if a series is given """
    if isinstance(array, ABCSeries):
        return array.values
    return array
