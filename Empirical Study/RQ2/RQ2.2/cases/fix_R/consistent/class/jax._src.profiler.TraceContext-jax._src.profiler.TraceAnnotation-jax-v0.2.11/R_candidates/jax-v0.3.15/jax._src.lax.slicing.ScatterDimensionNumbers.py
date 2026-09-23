class ScatterDimensionNumbers(NamedTuple):
  """
  Describes the dimension number arguments to an `XLA's Scatter operator
  <https://www.tensorflow.org/xla/operation_semantics#scatter>`_. See the XLA
  documentation for more details of what the dimension numbers mean.

  Args:
    update_window_dims: the set of dimensions in the `updates` that are window
      dimensions. Must be a tuple of integers in ascending
      order, each representing a dimension number.
    inserted_window_dims: the set of size 1 window dimensions that must be
      inserted into the shape of `updates`. Must be a tuple of integers in
      ascending order, each representing a dimension number of the output. These
      are the mirror image of `collapsed_slice_dims` in the case of `gather`.
    scatter_dims_to_operand_dims: for each dimension in `scatter_indices`, gives
      the corresponding dimension in `operand`. Must be a sequence of integers
      with size equal to indices.shape[-1].

  Unlike XLA's `ScatterDimensionNumbers` structure, `index_vector_dim` is
  implicit; there is always an index vector dimension and it must always be the
  last dimension. To scatter scalar indices, add a trailing dimension of size 1.
  """
  update_window_dims: Sequence[int]
  inserted_window_dims: Sequence[int]
  scatter_dims_to_operand_dims: Sequence[int]
