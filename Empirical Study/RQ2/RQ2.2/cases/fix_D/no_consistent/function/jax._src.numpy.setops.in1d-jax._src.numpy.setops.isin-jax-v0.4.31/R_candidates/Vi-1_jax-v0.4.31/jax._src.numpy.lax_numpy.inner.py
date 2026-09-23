@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def inner(
    a: ArrayLike, b: ArrayLike, *, precision: PrecisionLike = None,
    preferred_element_type: DType | None = None,
) -> Array:
  """Compute the inner product of two arrays.

  JAX implementation of :func:`numpy.inner`.

  Unlike :func:`jax.numpy.matmul` or :func:`jax.numpy.dot`, this always performs
  a contraction along the last dimension of each input.

  Args:
    a: array of shape ``(..., N)``
    b: array of shape ``(..., N)``
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array of shape ``(*a.shape[:-1], *b.shape[:-1])`` containing the batched vector
    product of the inputs.

  See also:
    - :func:`jax.numpy.vecdot`: conjugate multiplication along a specified axis.
    - :func:`jax.numpy.tensordot`: general tensor multiplication.
    - :func:`jax.numpy.matmul`: general batched matrix & vector multiplication.

  Examples:
    For 1D inputs, this implements standard (non-conjugate) vector multiplication:

    >>> a = jnp.array([1j, 3j, 4j])
    >>> b = jnp.array([4., 2., 5.])
    >>> jnp.inner(a, b)
    Array(0.+30.j, dtype=complex64)

    For multi-dimensional inputs, batch dimensions are stacked rather than broadcast:

    >>> a = jnp.ones((2, 3))
    >>> b = jnp.ones((5, 3))
    >>> jnp.inner(a, b).shape
    (2, 5)
  """
  util.check_arraylike("inner", a, b)
  if ndim(a) == 0 or ndim(b) == 0:
    a = asarray(a, dtype=preferred_element_type)
    b = asarray(b, dtype=preferred_element_type)
    return a * b
  return tensordot(a, b, (-1, -1), precision=precision,
                   preferred_element_type=preferred_element_type)
