def copy(a: ArrayLike, order: str | None = None) -> Array:
  """Return a copy of the array.

  JAX implementation of :func:`numpy.copy`.

  Args:
    a: arraylike object to copy
    order: not implemented in JAX

  Returns:
    a copy of the input array ``a``.

  See Also:
    - :func:`jax.numpy.array`: create an array with or without a copy.
    - :meth:`jax.Array.copy`: same function accessed as an array method.

  Examples:
    Since JAX arrays are immutable, in most cases explicit array copies
    are not necessary. One exception is when using a function with donated
    arguments (see the ``donate_argnums`` argument to :func:`jax.jit`).

    >>> f = jax.jit(lambda x: 2 * x, donate_argnums=0)
    >>> x = jnp.arange(4)
    >>> y = f(x)
    >>> print(y)
    [0 2 4 6]

    Because we marked ``x`` as being donated, the original array is no longer
    available:

    >>> print(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    RuntimeError: Array has been deleted with shape=int32[4].

    In situations like this, an explicit copy will let you keep access to the
    original buffer:

    >>> x = jnp.arange(4)
    >>> y = f(x.copy())
    >>> print(y)
    [0 2 4 6]
    >>> print(x)
    [0 1 2 3]
  """
  util.check_arraylike("copy", a)
  return array(a, copy=True, order=order)
