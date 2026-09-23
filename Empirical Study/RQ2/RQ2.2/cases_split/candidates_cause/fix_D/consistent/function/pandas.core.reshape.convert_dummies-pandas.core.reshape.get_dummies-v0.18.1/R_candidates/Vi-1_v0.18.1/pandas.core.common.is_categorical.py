def is_categorical(array):
    """ return if we are a categorical possibility """
    return isinstance(array, gt.ABCCategorical) or is_categorical_dtype(array)
