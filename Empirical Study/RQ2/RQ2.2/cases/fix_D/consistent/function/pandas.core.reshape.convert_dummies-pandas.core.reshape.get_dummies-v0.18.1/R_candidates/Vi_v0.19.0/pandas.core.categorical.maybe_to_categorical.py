def maybe_to_categorical(array):
    """ coerce to a categorical if a series is given """
    if isinstance(array, (ABCSeries, ABCCategoricalIndex)):
        return array._values
    return array
