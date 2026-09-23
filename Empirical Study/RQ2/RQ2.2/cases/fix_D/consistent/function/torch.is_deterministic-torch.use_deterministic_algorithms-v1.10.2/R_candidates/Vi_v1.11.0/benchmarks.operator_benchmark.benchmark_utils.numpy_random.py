def numpy_random(dtype, *shapes):
    """ Return a random numpy tensor of the provided dtype.
        Args:
            shapes: int or a sequence of ints to defining the shapes of the tensor
            dtype: use the dtypes from numpy
                (https://docs.scipy.org/doc/numpy/user/basics.types.html)
        Return:
            numpy tensor of dtype
    """
    # TODO: consider more complex/custom dynamic ranges for
    # comprehensive test coverage.
    return np.random.rand(*shapes).astype(dtype)
