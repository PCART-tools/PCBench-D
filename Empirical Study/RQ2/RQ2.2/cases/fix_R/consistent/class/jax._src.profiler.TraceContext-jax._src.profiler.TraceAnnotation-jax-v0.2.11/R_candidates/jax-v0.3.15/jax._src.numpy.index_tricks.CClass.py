class CClass(_AxisConcat):
  """Concatenate slices, scalars and array-like objects along the last axis.

  LAX-backend implementation of :obj:`numpy.c_`.

  See Also:
    ``jnp.r_``: Concatenates slices, scalars and array-like objects along the first axis.

  Examples:

    >>> a = jnp.arange(6).reshape((2,3))
    >>> jnp.c_[a,a]
    DeviceArray([[0, 1, 2, 0, 1, 2],
                 [3, 4, 5, 3, 4, 5]], dtype=int32)

    Use a string directive of the form ``"axis:dims:trans1d"`` as the first argument to specify
    concatenation axis, minimum number of dimensions, and the position of the upgraded array's
    original dimensions in the resulting array's shape tuple:

    >>> jnp.c_['0,2', [1,2,3], [4,5,6]]
    DeviceArray([[1],
                 [2],
                 [3],
                 [4],
                 [5],
                 [6]], dtype=int32)

    >>> jnp.c_['0,2,-1', [1,2,3], [4,5,6]]
    DeviceArray([[1, 2, 3],
                 [4, 5, 6]], dtype=int32)

    Use the special directives ``"r"`` or ``"c"`` as the first argument on flat inputs
    to create an array with inputs stacked along the last axis:

    >>> jnp.c_['r',[1,2,3], [4,5,6]]
    DeviceArray([[1, 4],
                 [2, 5],
                 [3, 6]], dtype=int32)
  """
  axis = -1
  ndmin = 2
  trans1d = 0
  op_name = "c_"
