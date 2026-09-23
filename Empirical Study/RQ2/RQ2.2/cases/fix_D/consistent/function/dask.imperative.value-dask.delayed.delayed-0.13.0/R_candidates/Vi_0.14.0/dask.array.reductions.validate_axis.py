def validate_axis(ndim, axis):
    """ Validate single axis dimension against number of dimensions """
    if axis > ndim - 1 or axis < -ndim:
        raise ValueError("Axis must be between -%d and %d, got %d" %
                         (ndim, ndim - 1, axis))
    if axis < 0:
        return axis + ndim
    else:
        return axis
