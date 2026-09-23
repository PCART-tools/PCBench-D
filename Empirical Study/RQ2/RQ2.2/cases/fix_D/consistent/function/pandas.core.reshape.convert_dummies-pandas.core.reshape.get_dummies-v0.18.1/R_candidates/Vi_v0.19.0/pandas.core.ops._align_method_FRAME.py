def _align_method_FRAME(left, right, axis):
    """ convert rhs to meet lhs dims if input is list, tuple or np.ndarray """

    def to_series(right):
        msg = 'Unable to coerce to Series, length must be {0}: given {1}'
        if axis is not None and left._get_axis_name(axis) == 'index':
            if len(left.index) != len(right):
                raise ValueError(msg.format(len(left.index), len(right)))
            right = left._constructor_sliced(right, index=left.index)
        else:
            if len(left.columns) != len(right):
                raise ValueError(msg.format(len(left.columns), len(right)))
            right = left._constructor_sliced(right, index=left.columns)
        return right

    if isinstance(right, (list, tuple)):
        right = to_series(right)

    elif isinstance(right, np.ndarray) and right.ndim:  # skips np scalar

        if right.ndim == 1:
            right = to_series(right)

        elif right.ndim == 2:
            if left.shape != right.shape:
                msg = ("Unable to coerce to DataFrame, "
                       "shape must be {0}: given {1}")
                raise ValueError(msg.format(left.shape, right.shape))

            right = left._constructor(right, index=left.index,
                                      columns=left.columns)
        else:
            msg = 'Unable to coerce to Series/DataFrame, dim must be <= 2: {0}'
            raise ValueError(msg.format(right.shape, ))

    return right
