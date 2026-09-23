def is_categorical(array):
    """ return if we are a categorical possibility """
    return isinstance(array, ABCCategorical) or isinstance(array.dtype, CategoricalDtype)
