@partial(jit, static_argnames=('axis1', 'axis2'), inline=True)
def swapaxes(a: ArrayLike, axis1: int, axis2: int) -> Array:
  """Swap two axes of an array.

  JAX implementation of :func:`numpy.swapaxes`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    a: input array
    axis1: index of first axis
    axis2: index of second axis

  Returns:
    Copy of ``a`` with specified axes swapped.

  Notes:
    Unlike :func:`numpy.swapaxes`, :func:`jax.numpy.swapaxes` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :func:`jax.numpy.moveaxis`: move a single axis of an array.
    - :func:`jax.numpy.rollaxis`: older API for ``moveaxis``.
    - :func:`jax.lax.transpose`: more general axes permutations.
    - :meth:`jax.Array.swapaxes`: same functionality via an array method.

  Examples:
    >>> a = jnp.ones((2, 3, 4, 5))
    >>> jnp.swapaxes(a, 1, 3).shape
    (2, 5, 4, 3)

    Equivalent output via the ``swapaxes`` array method:

    >>> a.swapaxes(1, 3).shape
    (2, 5, 4, 3)

    Equivalent output via :func:`~jax.numpy.transpose`:

    >>> a.transpose(0, 3, 2, 1).shape
    (2, 5, 4, 3)
  """
  util.check_arraylike("swapaxes", a)
  perm = np.arange(ndim(a))
  perm[axis1], perm[axis2] = perm[axis2], perm[axis1]
  return lax.transpose(a, list(perm))
