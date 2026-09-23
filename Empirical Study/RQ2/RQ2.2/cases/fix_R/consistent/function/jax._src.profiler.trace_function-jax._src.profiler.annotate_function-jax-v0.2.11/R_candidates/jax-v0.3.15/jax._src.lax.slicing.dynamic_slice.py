def dynamic_slice(operand: Array, start_indices: Sequence[Array],
                  slice_sizes: Shape) -> Array:
  """Wraps XLA's `DynamicSlice
  <https://www.tensorflow.org/xla/operation_semantics#dynamicslice>`_
  operator.

  Args:
    operand: an array to slice.
    start_indices: a list of scalar indices, one per dimension. These values
      may be dynamic.
    slice_sizes: the size of the slice. Must be a sequence of non-negative
      integers with length equal to `ndim(operand)`. Inside a JIT compiled
      function, only static values are supported (all JAX arrays inside JIT
      must have statically known size).

  Returns:
    An array containing the slice.

  Examples:
    Here is a simple two-dimensional dynamic slice:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    DeviceArray([[ 0,  1,  2,  3],
                 [ 4,  5,  6,  7],
                 [ 8,  9, 10, 11]], dtype=int32)

    >>> dynamic_slice(x, (1, 1), (2, 3))
    DeviceArray([[ 5,  6,  7],
                 [ 9, 10, 11]], dtype=int32)

    Note the potentially surprising behavior for the case where the requested slice
    overruns the bounds of the array; in this case the start index is adjusted to
    return a slice of the requested size:

    >>> dynamic_slice(x, (1, 1), (2, 4))
    DeviceArray([[ 4,  5,  6,  7],
                 [ 8,  9, 10, 11]], dtype=int32)
  """
  start_indices = _dynamic_slice_indices(operand, start_indices)
  return dynamic_slice_p.bind(operand, *start_indices,
                              slice_sizes=core.canonicalize_shape(slice_sizes))
