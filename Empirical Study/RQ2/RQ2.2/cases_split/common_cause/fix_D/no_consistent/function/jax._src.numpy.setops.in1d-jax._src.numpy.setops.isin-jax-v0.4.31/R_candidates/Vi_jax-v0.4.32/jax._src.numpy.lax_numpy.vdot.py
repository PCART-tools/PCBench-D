@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def vdot(
    a: ArrayLike, b: ArrayLike, *,
    precision: PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
) -> Array:
  """Perform a conjugate multiplication of two 1D vectors.

  JAX implementation of :func:`numpy.vdot`.

  Args:
    a: first input array, if not 1D it will be flattened.
    b: second input array, if not 1D it will be flattened. Must have ``a.size == b.size``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    Scalar array (shape ``()``) containing the conjugate vector product of the inputs.

  See Also:
    - :func:`jax.numpy.vecdot`: batched vector product.
    - :func:`jax.numpy.matmul`: general matrix multiplication.
    - :func:`jax.lax.dot_general`: general N-dimensional batched dot product.

  Examples:
    >>> x = jnp.array([1j, 2j, 3j])
    >>> y = jnp.array([1., 2., 3.])
    >>> jnp.vdot(x, y)
    Array(0.-14.j, dtype=complex64)

    Note the difference between this and :func:`~jax.numpy.dot`, which does not
    conjugate the first input when complex:

    >>> jnp.dot(x, y)
    Array(0.+14.j, dtype=complex64)
  """
  util.check_arraylike("vdot", a, b)
  if issubdtype(_dtype(a), complexfloating):
    a = ufuncs.conj(a)
  return dot(ravel(a), ravel(b), precision=precision,
             preferred_element_type=preferred_element_type)
