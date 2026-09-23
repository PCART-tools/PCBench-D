def flatnonzero(a: ArrayLike, *, size: int | None = None,
                fill_value: None | ArrayLike | tuple[ArrayLike, ...] = None) -> Array:
  """Return indices of nonzero elements in a flattened array

  JAX implementation of :func:`numpy.flatnonzero`.

  ``jnp.flatnonzero(x)`` is equivalent to ``nonzero(ravel(a))[0]``. For a full
  discussion of the parameters to this function, refer to :func:`jax.numpy.nonzero`.

  Args:
    a: N-dimensional array.
    size: optional static integer specifying the number of nonzero entries to
      return. See :func:`jax.numpy.nonzero` for more discussion of this parameter.
    fill_value: optional padding value when ``size`` is specified. Defaults to 0.
      See :func:`jax.numpy.nonzero` for more discussion of this parameter.

  Returns:
    Array containing the indices of each nonzero value in the flattened array.

  See Also:
    - :func:`jax.numpy.nonzero`
    - :func:`jax.numpy.where`

  Examples:
    >>> x = jnp.array([[0, 5, 0],
    ...                [6, 0, 8]])
    >>> jnp.flatnonzero(x)
    Array([1, 3, 5], dtype=int32)

    This is equivalent to calling :func:`~jax.numpy.nonzero` on the flattened
    array, and extracting the first entry in the resulting tuple:

    >>> jnp.nonzero(x.ravel())[0]
    Array([1, 3, 5], dtype=int32)

    The returned indices can be used to extract nonzero entries from the
    flattened array:

    >>> indices = jnp.flatnonzero(x)
    >>> x.ravel()[indices]
    Array([5, 6, 8], dtype=int32)
  """
  return nonzero(ravel(a), size=size, fill_value=fill_value)[0]
