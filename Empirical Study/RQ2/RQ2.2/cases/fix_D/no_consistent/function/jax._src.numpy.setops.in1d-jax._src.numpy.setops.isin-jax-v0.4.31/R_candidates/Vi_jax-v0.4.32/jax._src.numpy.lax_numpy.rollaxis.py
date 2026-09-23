@partial(jit, static_argnames=('axis', 'start'))
def rollaxis(a: ArrayLike, axis: int, start: int = 0) -> Array:
  """Roll the specified axis to a given position.

  JAX implementation of :func:`numpy.rollaxis`.

  This function exists for compatibility with NumPy, but in most cases the newer
  :func:`jax.numpy.moveaxis` instead, because the meaning of its arguments is
  more intuitive.

  Args:
    a: input array.
    axis: index of the axis to roll forward.
    start: index toward which the axis will be rolled (default = 0). After
      normalizing negative axes, if ``start <= axis``, the axis is rolled to
      the ``start`` index; if ``start > axis``, the axis is rolled until the
      position before ``start``.

  Returns:
    Copy of ``a`` with rolled axis.

  Notes:
    Unlike :func:`numpy.rollaxis`, :func:`jax.numpy.rollaxis` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize away
    such copies when possible, so this doesn't have performance impacts in practice.

  See also:
    - :func:`jax.numpy.moveaxis`: newer API with clearer semantics than ``rollaxis``;
      this should be preferred to ``rollaxis`` in most cases.
    - :func:`jax.numpy.swapaxes`: swap two axes.
    - :func:`jax.numpy.transpose`: general permutation of axes.

  Examples:
    >>> a = jnp.ones((2, 3, 4, 5))

    Roll axis 2 to the start of the array:

    >>> jnp.rollaxis(a, 2).shape
    (4, 2, 3, 5)

    Roll axis 1 to the end of the array:

    >>> jnp.rollaxis(a, 1, a.ndim).shape
    (2, 4, 5, 3)

    Equivalent of these two with :func:`~jax.numpy.moveaxis`

    >>> jnp.moveaxis(a, 2, 0).shape
    (4, 2, 3, 5)
    >>> jnp.moveaxis(a, 1, -1).shape
    (2, 4, 5, 3)
  """
  util.check_arraylike("rollaxis", a)
  start = core.concrete_or_error(operator.index, start, "'start' argument of jnp.rollaxis()")
  a_ndim = ndim(a)
  axis = _canonicalize_axis(axis, a_ndim)
  if not (-a_ndim <= start <= a_ndim):
    raise ValueError(f"{start=} must satisfy {-a_ndim}<=start<={a_ndim}")
  if start < 0:
    start += a_ndim
  if start > axis:
    start -= 1
  return moveaxis(a, axis, start)
