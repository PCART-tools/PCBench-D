@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def dot(a: ArrayLike, b: ArrayLike, *,
        precision: PrecisionLike = None,
        preferred_element_type: DTypeLike | None = None) -> Array:
  """Compute the dot product of two arrays.

  JAX implementation of :func:`numpy.dot`.

  This differs from :func:`jax.numpy.matmul` in two respects:

  - if either ``a`` or ``b`` is a scalar, the result of ``dot`` is equivalent to
    :func:`jax.numpy.multiply`, while the result of ``matmul`` is an error.
  - if ``a`` and ``b`` have more than 2 dimensions, the batch indices are
    stacked rather than broadcast.

  Args:
    a: first input array, of shape ``(..., N)``.
    b: second input array. Must have shape ``(N,)`` or ``(..., N, M)``.
      In the multi-dimensional case, leading dimensions must be broadcast-compatible
      with the leading dimensions of ``a``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the dot product of the inputs, with batch dimensions of
    ``a`` and ``b`` stacked rather than broadcast.

  See also:
    - :func:`jax.numpy.matmul`: broadcasted batched matmul.
    - :func:`jax.lax.dot_general`: general batched matrix multiplication.

  Examples:
    For scalar inputs, ``dot`` computes the element-wise product:

    >>> x = jnp.array([1, 2, 3])
    >>> jnp.dot(x, 2)
    Array([2, 4, 6], dtype=int32)

    For vector or matrix inputs, ``dot`` computes the vector or matrix product:

    >>> M = jnp.array([[2, 3, 4],
    ...                [5, 6, 7],
    ...                [8, 9, 0]])
    >>> jnp.dot(M, x)
    Array([20, 38, 26], dtype=int32)
    >>> jnp.dot(M, M)
    Array([[ 51,  60,  29],
           [ 96, 114,  62],
           [ 61,  78,  95]], dtype=int32)

    For higher-dimensional matrix products, batch dimensions are stacked, whereas
    in :func:`~jax.numpy.matmul` they are broadcast. For example:

    >>> a = jnp.zeros((3, 2, 4))
    >>> b = jnp.zeros((3, 4, 1))
    >>> jnp.dot(a, b).shape
    (3, 2, 3, 1)
    >>> jnp.matmul(a, b).shape
    (3, 2, 1)
  """
  util.check_arraylike("dot", a, b)
  dtypes.check_user_dtype_supported(preferred_element_type, "dot")
  a, b = asarray(a), asarray(b)
  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(a, b, return_weak_type_flag=True)
  else:
    output_weak_type = False

  batch_dims = ((), ())
  a_ndim, b_ndim = ndim(a), ndim(b)
  if a_ndim == 0 or b_ndim == 0:
    # TODO(jakevdp): lower this case to dot_general as well?
    # Currently, doing so causes issues in remat tests due to #16805
    if preferred_element_type is not None:
      a = a.astype(preferred_element_type)
      b = b.astype(preferred_element_type)
    result = lax.mul(a, b)
  else:
    if b_ndim == 1:
      contract_dims = ((a_ndim - 1,), (0,))
    else:
      contract_dims = ((a_ndim - 1,), (b_ndim - 2,))
    result = lax.dot_general(a, b, dimension_numbers=(contract_dims, batch_dims),
                             precision=precision, preferred_element_type=preferred_element_type)
  return lax_internal._convert_element_type(result, preferred_element_type, output_weak_type)
