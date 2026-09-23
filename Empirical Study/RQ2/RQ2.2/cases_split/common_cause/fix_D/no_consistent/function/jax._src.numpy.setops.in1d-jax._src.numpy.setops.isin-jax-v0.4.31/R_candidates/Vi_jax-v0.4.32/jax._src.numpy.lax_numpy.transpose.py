def transpose(a: ArrayLike, axes: Sequence[int] | None = None) -> Array:
  """Return a transposed version of an N-dimensional array.

  JAX implementation of :func:`numpy.transpose`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    a: input array
    axes: optionally specify the permutation using a length-`a.ndim` sequence of integers
      ``i`` satisfying ``0 <= i < a.ndim``. Defaults to ``range(a.ndim)[::-1]``, i.e.
      reverses the order of all axes.

  Returns:
    transposed copy of the array.

  See Also:
    - :func:`jax.Array.transpose`: equivalent function via an :class:`~jax.Array` method.
    - :attr:`jax.Array.T`: equivalent function via an :class:`~jax.Array`  property.
    - :func:`jax.numpy.matrix_transpose`: transpose the last two axes of an array. This is
      suitable for working with batched 2D matrices.
    - :func:`jax.numpy.swapaxes`: swap any two axes in an array.
    - :func:`jax.numpy.moveaxis`: move an axis to another position in the array.

  Note:
    Unlike :func:`numpy.transpose`, :func:`jax.numpy.transpose` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  Examples:
    For a 1D array, the transpose is the identity:

    >>> x = jnp.array([1, 2, 3, 4])
    >>> jnp.transpose(x)
    Array([1, 2, 3, 4], dtype=int32)

    For a 2D array, the transpose is a matrix transpose:

    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.transpose(x)
    Array([[1, 3],
           [2, 4]], dtype=int32)

    For an N-dimensional array, the transpose reverses the order of the axes:

    >>> x = jnp.zeros(shape=(3, 4, 5))
    >>> jnp.transpose(x).shape
    (5, 4, 3)

    The ``axes`` argument can be specified to change this default behavior:

    >>> jnp.transpose(x, (0, 2, 1)).shape
    (3, 5, 4)

    Since swapping the last two axes is a common operation, it can be done
    via its own API, :func:`jax.numpy.matrix_transpose`:

    >>> jnp.matrix_transpose(x).shape
    (3, 5, 4)

    For convenience, transposes may also be performed using the :meth:`jax.Array.transpose`
    method or the :attr:`jax.Array.T` property:

    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> x.transpose()
    Array([[1, 3],
           [2, 4]], dtype=int32)
    >>> x.T
    Array([[1, 3],
           [2, 4]], dtype=int32)
  """
  util.check_arraylike("transpose", a)
  axes_ = list(range(ndim(a))[::-1]) if axes is None else axes
  axes_ = [_canonicalize_axis(i, ndim(a)) for i in axes_]
  return lax.transpose(a, axes_)
