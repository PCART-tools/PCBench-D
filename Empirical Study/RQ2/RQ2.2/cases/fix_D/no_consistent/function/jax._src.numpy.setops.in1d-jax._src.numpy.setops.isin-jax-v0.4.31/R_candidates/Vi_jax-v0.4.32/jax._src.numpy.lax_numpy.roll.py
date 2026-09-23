def roll(a: ArrayLike, shift: ArrayLike | Sequence[int],
         axis: int | Sequence[int] | None = None) -> Array:
  """Roll the elements of an array along a specified axis.

  JAX implementation of :func:`numpy.roll`.

  Args:
    a: input array.
    shift: the number of positions to shift the specified axis. If an integer,
      all axes are shifted by the same amount. If a tuple, the shift for each
      axis is specified individually.
    axis: the axis or axes to roll. If ``None``, the array is flattened, shifted,
      and then reshaped to its original shape.

  Returns:
    A copy of ``a`` with elements rolled along the specified axis or axes.

  See also:
    - :func:`jax.numpy.rollaxis`: roll the specified axis to a given position.

  Examples:
    >>> a = jnp.array([0, 1, 2, 3, 4, 5])
    >>> jnp.roll(a, 2)
    Array([4, 5, 0, 1, 2, 3], dtype=int32)

    Roll elements along a specific axis:

    >>> a = jnp.array([[ 0,  1,  2,  3],
    ...                [ 4,  5,  6,  7],
    ...                [ 8,  9, 10, 11]])
    >>> jnp.roll(a, 1, axis=0)
    Array([[ 8,  9, 10, 11],
           [ 0,  1,  2,  3],
           [ 4,  5,  6,  7]], dtype=int32)
    >>> jnp.roll(a, [2, 3], axis=[0, 1])
    Array([[ 5,  6,  7,  4],
           [ 9, 10, 11,  8],
           [ 1,  2,  3,  0]], dtype=int32)
  """
  util.check_arraylike("roll", a)
  arr = asarray(a)
  if axis is None:
    return roll(arr.ravel(), shift, 0).reshape(arr.shape)
  axis = _ensure_index_tuple(axis)
  axis = tuple(_canonicalize_axis(ax, arr.ndim) for ax in axis)
  try:
    shift = _ensure_index_tuple(shift)
  except TypeError:
    return _roll_dynamic(arr, asarray(shift), axis)
  else:
    return _roll_static(arr, shift, axis)
