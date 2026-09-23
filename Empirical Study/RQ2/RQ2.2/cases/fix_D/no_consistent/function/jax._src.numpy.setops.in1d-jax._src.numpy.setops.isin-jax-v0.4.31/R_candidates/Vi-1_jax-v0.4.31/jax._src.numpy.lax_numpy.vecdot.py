def vecdot(x1: ArrayLike, x2: ArrayLike, /, *, axis: int = -1,
           precision: PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  """Perform a conjugate multiplication of two batched vectors.

  JAX implementation of :func:`numpy.vecdot`.

  Args:
    a: left-hand side array.
    b: right-hand side array. Size of ``b[axis]`` must match size of ``a[axis]``,
      and remaining dimensions must be broadcast-compatible.
    axis: axis along which to compute the dot product (default: -1)
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the conjugate dot product of ``a`` and ``b`` along ``axis``.
    The non-contracted dimensions are broadcast together.

  See Also:
    - :func:`jax.numpy.vdot`: flattened vector product.
    - :func:`jax.numpy.matmul`: general matrix multiplication.
    - :func:`jax.lax.dot_general`: general N-dimensional batched dot product.

  Examples:
    Vector conjugate-dot product of two 1D arrays:

    >>> a = jnp.array([1j, 2j, 3j])
    >>> b = jnp.array([4., 5., 6.])
    >>> jnp.linalg.vecdot(a, b)
    Array(0.-32.j, dtype=complex64)

    Batched vector dot product of two 2D arrays:

    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> b = jnp.array([[2, 3, 4]])
    >>> jnp.linalg.vecdot(a, b, axis=-1)
    Array([20, 47], dtype=int32)
  """
  util.check_arraylike("jnp.vecdot", x1, x2)
  x1_arr, x2_arr = asarray(x1), asarray(x2)
  if x1_arr.shape[axis] != x2_arr.shape[axis]:
    raise ValueError(f"axes must match; got shapes {x1_arr.shape} and {x2_arr.shape} with {axis=}")
  x1_arr = jax.numpy.moveaxis(x1_arr, axis, -1)
  x2_arr = jax.numpy.moveaxis(x2_arr, axis, -1)
  return vectorize(partial(vdot, precision=precision, preferred_element_type=preferred_element_type),
                   signature="(n),(n)->()")(x1_arr, x2_arr)
