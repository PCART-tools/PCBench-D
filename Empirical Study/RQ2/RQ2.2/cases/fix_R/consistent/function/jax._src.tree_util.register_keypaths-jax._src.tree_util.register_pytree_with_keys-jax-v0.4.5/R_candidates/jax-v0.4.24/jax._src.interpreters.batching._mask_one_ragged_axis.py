def _mask_one_ragged_axis(
    operand: Array, ident, axis_spec: RaggedAxis) -> Array:
  assert len(axis_spec.ragged_axes) == 1, "Mask just one ragged axis at a time"
  ragged_axis, segment_lengths = axis_spec.ragged_axes[0]
  value = ident(operand.dtype)
  positions = jax.lax.broadcasted_iota('int32', operand.shape, ragged_axis)
  # TODO(mattjj, axch) can't get ._data, need to convert it
  # lengths = jax.lax.convert_element_type(segment_lengths._data, 'int32')
  lengths = jax.lax.convert_element_type(segment_lengths, 'int32')
  limits = jax.lax.broadcast_in_dim(
      lengths, operand.shape, [axis_spec.stacked_axis])
  mask = positions < limits
  return jax.lax.select(mask, operand, jax.lax.broadcast(value, operand.shape))
