def dot_general(lhs: ArrayLike, rhs: ArrayLike, dimension_numbers: DotDimensionNumbers,
                precision: PrecisionLike = None,
                preferred_element_type: DTypeLike | None = None) -> Array:
  """General dot product/contraction operator.

  Wraps XLA's `DotGeneral
  <https://www.tensorflow.org/xla/operation_semantics#dotgeneral>`_
  operator.

  The semantics of ``dot_general`` are complicated, but most users should not have to
  use it directly. Instead, you can use higher-level functions like :func:`jax.numpy.dot`,
  :func:`jax.numpy.matmul`, :func:`jax.numpy.tensordot`, :func:`jax.numpy.einsum`,
  and others which will construct appropriate calls to ``dot_general`` under the hood.
  If you really want to understand ``dot_general`` itself, we recommend reading XLA's
  `DotGeneral  <https://www.tensorflow.org/xla/operation_semantics#dotgeneral>`_
  operator documentation.

  Args:
    lhs: an array
    rhs: an array
    dimension_numbers: a tuple of tuples of sequences of ints of the form
      ``((lhs_contracting_dims, rhs_contracting_dims), (lhs_batch_dims, rhs_batch_dims))``
    precision: Optional. Either ``None``, which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      :class:`~jax.lax.Precision` enums indicating precision of ``lhs``` and ``rhs``.
    preferred_element_type: Optional. Either ``None``, which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    An array whose first dimensions are the (shared) batch dimensions, followed by
    the ``lhs`` non-contracting/non-batch dimensions, and finally the ``rhs``
    non-contracting/non-batch dimensions.
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
