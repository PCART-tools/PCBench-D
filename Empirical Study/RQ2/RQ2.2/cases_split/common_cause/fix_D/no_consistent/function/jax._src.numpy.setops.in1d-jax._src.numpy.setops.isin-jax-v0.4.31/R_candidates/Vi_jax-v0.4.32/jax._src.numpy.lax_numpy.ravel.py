@partial(jit, static_argnames=('order',), inline=True)
def ravel(a: ArrayLike, order: str = "C") -> Array:
  """Flatten array into a 1-dimensional shape.

  JAX implementation of :func:`numpy.ravel`, implemented in terms of
  :func:`jax.lax.reshape`.

  ``ravel(arr, order=order)`` is equivalent to ``reshape(arr, -1, order=order)``.

  Args:
    a: array to be flattened.
    order: ``'F'`` or ``'C'``, specifies whether the reshape should apply column-major
      (fortran-style, ``"F"``) or row-major (C-style, ``"C"``) order; default is ``"C"``.
      JAX does not support `order="A"` or `order="K"`.

  Returns:
    flattened copy of input array.

  Notes:
    Unlike :func:`numpy.ravel`, :func:`jax.numpy.ravel` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :meth:`jax.Array.ravel`: equivalent functionality via an array method.
    - :func:`jax.numpy.reshape`: general array reshape.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])

    By default, ravel in C-style, row-major order

    >>> jnp.ravel(x)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)

    Optionally ravel in Fortran-style, column-major:

    >>> jnp.ravel(x, order='F')
    Array([1, 4, 2, 5, 3, 6], dtype=int32)

    For convenience, the same functionality is available via the :meth:`jax.Array.ravel`
    method:

    >>> x.ravel()
    Array([1, 2, 3, 4, 5, 6], dtype=int32)
  """
  util.check_arraylike("ravel", a)
  if order == "K":
    raise NotImplementedError("Ravel not implemented for order='K'.")
  return reshape(a, (size(a),), order)
