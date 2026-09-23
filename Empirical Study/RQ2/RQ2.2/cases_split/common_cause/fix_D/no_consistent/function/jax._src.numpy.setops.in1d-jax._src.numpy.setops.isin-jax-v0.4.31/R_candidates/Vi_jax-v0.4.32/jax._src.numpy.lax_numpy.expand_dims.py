def expand_dims(a: ArrayLike, axis: int | Sequence[int]) -> Array:
  """Insert dimensions of length 1 into array

  JAX implementation of :func:`numpy.expand_dims`, implemented via
  :func:`jax.lax.expand_dims`.

  Args:
    a: input array
    axis: integer or sequence of integers specifying positions of axes to add.

  Returns:
    Copy of ``a`` with added dimensions.

  Notes:
    Unlike :func:`numpy.expand_dims`, :func:`jax.numpy.expand_dims` will return a copy
    rather than a view of the input array. However, under JIT, the compiler will optimize
    away such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :func:`jax.numpy.squeeze`: inverse of this operation, i.e. remove length-1 dimensions.
    - :func:`jax.lax.expand_dims`: XLA version of this functionality.

  Examples:
    >>> x = jnp.array([1, 2, 3])
    >>> x.shape
    (3,)

    Expand the leading dimension:

    >>> jnp.expand_dims(x, 0)
    Array([[1, 2, 3]], dtype=int32)
    >>> _.shape
    (1, 3)

    Expand the trailing dimension:

    >>> jnp.expand_dims(x, 1)
    Array([[1],
           [2],
           [3]], dtype=int32)
    >>> _.shape
    (3, 1)

    Expand multiple dimensions:

    >>> jnp.expand_dims(x, (0, 1, 3))
    Array([[[[1],
             [2],
             [3]]]], dtype=int32)
    >>> _.shape
    (1, 1, 3, 1)

    Dimensions can also be expanded more succinctly by indexing with ``None``:

    >>> x[None]  # equivalent to jnp.expand_dims(x, 0)
    Array([[1, 2, 3]], dtype=int32)
    >>> x[:, None]  # equivalent to jnp.expand_dims(x, 1)
    Array([[1],
           [2],
           [3]], dtype=int32)
    >>> x[None, None, :, None]  # equivalent to jnp.expand_dims(x, (0, 1, 3))
    Array([[[[1],
             [2],
             [3]]]], dtype=int32)
  """
  util.check_arraylike("expand_dims", a)
  axis = _ensure_index_tuple(axis)
  return lax.expand_dims(a, axis)
