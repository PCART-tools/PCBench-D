@partial(jit, static_argnames=('axis',))
def append(
    arr: ArrayLike, values: ArrayLike, axis: int | None = None
) -> Array:
  """Return a new array with values appended to the end of the original array.

  JAX implementation of :func:`numpy.append`.

  Args:
    arr: original array.
    values: values to be appended to the array. The ``values`` must have
      the same number of dimensions as ``arr``, and all dimensions must
      match except in the specified axis.
    axis: axis along which to append values. If None (default), both ``arr``
      and ``values`` will be flattened before appending.

  Returns:
    A new array with values appended to ``arr``.

  See also:
    - :func:`jax.numpy.insert`
    - :func:`jax.numpy.delete`

  Examples:
    >>> a = jnp.array([1, 2, 3])
    >>> b = jnp.array([4, 5, 6])
    >>> jnp.append(a, b)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)

    Appending along a specific axis:

    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> b = jnp.array([[5, 6]])
    >>> jnp.append(a, b, axis=0)
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)

    Appending along a trailing axis:

    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> b = jnp.array([[7], [8]])
    >>> jnp.append(a, b, axis=1)
    Array([[1, 2, 3, 7],
           [4, 5, 6, 8]], dtype=int32)
  """
  if axis is None:
    return concatenate([ravel(arr), ravel(values)], 0)
  else:
    return concatenate([arr, values], axis=axis)
