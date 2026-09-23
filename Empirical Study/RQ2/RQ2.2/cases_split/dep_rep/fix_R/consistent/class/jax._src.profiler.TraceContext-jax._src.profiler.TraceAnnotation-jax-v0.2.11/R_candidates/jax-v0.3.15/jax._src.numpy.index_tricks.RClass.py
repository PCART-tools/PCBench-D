class RClass(_AxisConcat):
  """Concatenate slices, scalars and array-like objects along the first axis.

  LAX-backend implementation of :obj:`numpy.r_`.

  See Also:
    ``jnp.c_``: Concatenates slices, scalars and array-like objects along the last axis.

  Examples:
    Passing slices in the form ``[start:stop:step]`` generates ``jnp.arange`` objects:

    >>> jnp.r_[-1:5:1, 0, 0, jnp.array([1,2,3])]
    DeviceArray([-1,  0,  1,  2,  3,  4,  0,  0,  1,  2,  3], dtype=int32)

    An imaginary value for ``step`` will create a ``jnp.linspace`` object instead,
    which includes the right endpoint:

    >>> jnp.r_[-1:1:6j, 0, jnp.array([1,2,3])]
    DeviceArray([-1.        , -0.6       , -0.20000002,  0.20000005,
                  0.6       ,  1.        ,  0.        ,  1.        ,
                  2.        ,  3.        ], dtype=float32)

    Use a string directive of the form ``"axis,dims,trans1d"`` as the first argument to
    specify concatenation axis, minimum number of dimensions, and the position of the
    upgraded array's original dimensions in the resulting array's shape tuple:

    >>> jnp.r_['0,2', [1,2,3], [4,5,6]] # concatenate along first axis, 2D output
    DeviceArray([[1, 2, 3],
                 [4, 5, 6]], dtype=int32)

    >>> jnp.r_['0,2,0', [1,2,3], [4,5,6]] # push last input axis to the front
    DeviceArray([[1],
                 [2],
                 [3],
                 [4],
                 [5],
                 [6]], dtype=int32)

    Negative values for ``trans1d`` offset the last axis towards the start
    of the shape tuple:

    >>> jnp.r_['0,2,-2', [1,2,3], [4,5,6]]
    DeviceArray([[1],
                 [2],
                 [3],
                 [4],
                 [5],
                 [6]], dtype=int32)

    Use the special directives ``"r"`` or ``"c"`` as the first argument on flat inputs
    to create an array with an extra row or column axis, respectively:

    >>> jnp.r_['r',[1,2,3], [4,5,6]]
    DeviceArray([[1, 2, 3, 4, 5, 6]], dtype=int32)

    >>> jnp.r_['c',[1,2,3], [4,5,6]]
    DeviceArray([[1],
                 [2],
                 [3],
                 [4],
                 [5],
                 [6]], dtype=int32)

    For higher-dimensional inputs (``dim >= 2``), both directives ``"r"`` and ``"c"``
    give the same result.
  """
  axis = 0
  ndmin = 1
  trans1d = -1
  op_name = "r_"
