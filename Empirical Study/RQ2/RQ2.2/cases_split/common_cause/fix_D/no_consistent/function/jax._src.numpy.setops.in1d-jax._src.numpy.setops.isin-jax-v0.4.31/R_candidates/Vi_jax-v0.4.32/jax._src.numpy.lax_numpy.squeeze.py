def squeeze(a: ArrayLike, axis: int | Sequence[int] | None = None) -> Array:
  """Remove one or more length-1 axes from array

  JAX implementation of :func:`numpy.sqeeze`, implemented via :func:`jax.lax.squeeze`.

  Args:
    a: input array
    axis: integer or sequence of integers specifying axes to remove. If any specified
      axis does not have a length of 1, an error is raised. If not specified, squeeze
      all length-1 axes in ``a``.

  Returns:
    copy of ``a`` with length-1 axes removed.

  Notes:
    Unlike :func:`numpy.squeeze`, :func:`jax.numpy.squeeze` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :func:`jax.numpy.expand_dims`: the inverse of ``squeeze``: add dimensions of length 1.
    - :meth:`jax.Array.squeeze`: equivalent functionality via an array method.
    - :func:`jax.lax.squeeze`: equivalent XLA API.
    - :func:`jax.numpy.ravel`: flatten an array into a 1D shape.
    - :func:`jax.numpy.reshape`: general array reshape.

  Examples:
    >>> x = jnp.array([[[0]], [[1]], [[2]]])
    >>> x.shape
    (3, 1, 1)

    Squeeze all length-1 dimensions:

    >>> jnp.squeeze(x)
    Array([0, 1, 2], dtype=int32)
    >>> _.shape
    (3,)

    Equivalent while specifying the axes explicitly:

    >>> jnp.squeeze(x, axis=(1, 2))
    Array([0, 1, 2], dtype=int32)

    Attempting to squeeze a non-unit axis results in an error:

    >>> jnp.squeeze(x, axis=0)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    ValueError: cannot select an axis to squeeze out which has size not equal to one, got shape=(3, 1, 1) and dimensions=(0,)

    For convenience, this functionality is also available via the
    :meth:`jax.Array.squeeze` method:

    >>> x.squeeze()
    Array([0, 1, 2], dtype=int32)
  """
  util.check_arraylike("squeeze", a)
  return _squeeze(asarray(a), _ensure_index_tuple(axis) if axis is not None else None)
