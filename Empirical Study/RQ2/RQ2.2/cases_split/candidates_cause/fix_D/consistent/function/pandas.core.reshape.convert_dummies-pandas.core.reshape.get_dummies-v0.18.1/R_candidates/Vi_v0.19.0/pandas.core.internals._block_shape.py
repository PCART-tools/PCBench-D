def _block_shape(values, ndim=1, shape=None):
    """ guarantee the shape of the values to be at least 1 d """
    if values.ndim < ndim:
        if shape is None:
            shape = values.shape
        values = values.reshape(tuple((1, ) + shape))
    return values
