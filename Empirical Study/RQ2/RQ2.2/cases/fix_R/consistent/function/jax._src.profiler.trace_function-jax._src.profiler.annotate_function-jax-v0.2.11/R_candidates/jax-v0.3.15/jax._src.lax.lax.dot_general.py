def dot_general(lhs: Array, rhs: Array, dimension_numbers: DotDimensionNumbers,
                precision: PrecisionLike = None,
                preferred_element_type: Optional[DType] = None) -> Array:
  """More general contraction operator.

  Wraps XLA's `DotGeneral
  <https://www.tensorflow.org/xla/operation_semantics#dotgeneral>`_
  operator.

  Args:
    lhs: an array
    rhs: an array
    dimension_numbers: a tuple of tuples of the form
      `((lhs_contracting_dims, rhs_contracting_dims),
      (lhs_batch_dims, rhs_batch_dims))`
    precision: Optional. Either ``None``, which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      :class:`~jax.lax.Precision` enums indicating precision of ``lhs``` and ``rhs``.
    preferred_element_type: Optional. Either ``None``, which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    An array containing the result.
  """
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  cdims = (api_util._ensure_index_tuple(lhs_contract),
           api_util._ensure_index_tuple(rhs_contract))
  bdims = (api_util._ensure_index_tuple(lhs_batch),
           api_util._ensure_index_tuple(rhs_batch))
  preferred_element_type = (
      None if preferred_element_type is None else
      dtypes.canonicalize_dtype(np.dtype(preferred_element_type)))
  return dot_general_p.bind(lhs, rhs,
                            dimension_numbers=(cdims, bdims),
                            precision=canonicalize_precision(precision),
                            preferred_element_type=preferred_element_type)
