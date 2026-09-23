def dot(lhs: Array, rhs: Array, precision: PrecisionLike = None,
        preferred_element_type: Optional[DType] = None) -> Array:
  """Vector/vector, matrix/vector, and matrix/matrix multiplication.

  Wraps XLA's `Dot
  <https://www.tensorflow.org/xla/operation_semantics#dot>`_
  operator.

  For more general contraction, see the `dot_general` operator.

  Args:
    lhs: an array of dimension 1 or 2.
    rhs: an array of dimension 1 or 2.
    precision: Optional. Either ``None``, which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      :class:`~jax.lax.Precision` enums indicating precision of ``lhs``` and ``rhs``.
    preferred_element_type: Optional. Either ``None``, which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    An array containing the product.
  """
  if 1 <= lhs.ndim <= 2 and 1 <= rhs.ndim <= 2 and core.symbolic_equal_dim(lhs.shape[-1], rhs.shape[0]):
    return dot_general(lhs, rhs, (((lhs.ndim - 1,), (0,)), ((), ())),
                       precision=precision,
                       preferred_element_type=preferred_element_type)
  else:
    raise TypeError("Incompatible shapes for dot: got {} and {}.".format(
        lhs.shape, rhs.shape))
