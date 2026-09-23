def broadcast_in_dim(operand: ArrayLike, shape: Shape,
                     broadcast_dimensions: Sequence[int]) -> Array:
  """Wraps XLA's `BroadcastInDim
  <https://www.tensorflow.org/xla/operation_semantics#broadcastindim>`_
  operator.

  Args:
    operand: an array
    shape: the shape of the target array
    broadcast_dimensions: to which dimension in the target shape each dimension
      of the operand shape corresponds to.  That is, dimension i of the operand
      becomes dimension broadcast_dimensions[i] of the result.

  Returns:
    An array containing the result.

  See Also:
    jax.lax.broadcast : simpler interface to add new leading dimensions.
  """
  if np.ndim(operand) == len(shape) and not len(broadcast_dimensions) and isinstance(operand, Array):
    return type_cast(Array, operand)
  if config.dynamic_shapes.value:
    # We must gate this behavior under a flag because otherwise the errors
    # raised are different (and have worse source provenance information).
    dyn_shape, static_shape = _extract_tracers_dyn_shape(shape)
  else:
    dyn_shape, static_shape = [], shape  # type: ignore
  return broadcast_in_dim_p.bind(
      operand, *dyn_shape, shape=tuple(static_shape),
      broadcast_dimensions=tuple(broadcast_dimensions))
