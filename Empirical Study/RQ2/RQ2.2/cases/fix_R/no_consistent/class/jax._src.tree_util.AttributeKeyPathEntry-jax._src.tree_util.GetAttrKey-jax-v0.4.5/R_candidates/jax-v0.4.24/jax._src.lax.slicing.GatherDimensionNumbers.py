class GatherDimensionNumbers(NamedTuple):
  """
  Describes the dimension number arguments to an `XLA's Gather operator
  <https://www.tensorflow.org/xla/operation_semantics#gather>`_. See the XLA
  documentation for more details of what the dimension numbers mean.

  Args:
    offset_dims: the set of dimensions in the `gather` output that offset into
      an array sliced from `operand`. Must be a tuple of integers in ascending
      order, each representing a dimension number of the output.
    collapsed_slice_dims: the set of dimensions `i` in `operand` that have
      `slice_sizes[i] == 1` and that should not have a corresponding dimension
      in the output of the gather. Must be a tuple of integers in ascending
      order.
    start_index_map: for each dimension in `start_indices`, gives the
      corresponding dimension in `operand` that is to be sliced. Must be a
      tuple of integers with size equal to `start_indices.shape[-1]`.

  Unlike XLA's `GatherDimensionNumbers` structure, `index_vector_dim` is
  implicit; there is always an index vector dimension and it must always be the
  last dimension. To gather scalar indices, add a trailing dimension of size 1.
  """
  offset_dims: tuple[int, ...]
  collapsed_slice_dims: tuple[int, ...]
  start_index_map: tuple[int, ...]
