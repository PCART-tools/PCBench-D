def _slice(operand, start_indices, dynamic_slice_sizes, static_slice_sizes,
           fill_value=0):
  """Similar to lax.dynamic_slice, but handles arrays with dynamic sizes.

  Returns fill_value instead of clamping start_indices for those elements that
  would overflow the side of the array.

  Args:
    operand: the array to slice
    start_indices: the offset of the start of the slice
    dynamic_slice_sizes: the true (unpadded) size of the slice
    static_slice_sizes: the padded size of the slice, which must be known at
      compile time. The static size must be larger than the dynamic size.
    fill_value: value with which to replace masked-out elements.
  Returns:
    An array with static shape `static_slice_sizes`, padded from its true
    (dynamic) size `dynamic_slice_sizes`.
  """
  # We must pad the input array so the dynamic_slice is guaranteed to fall
  # entirely in bounds.
  padded = lax.pad(operand,
                   jnp.array(0, operand.dtype),
                   [(0, d, 0) for d in static_slice_sizes])
  out = lax.dynamic_slice(padded, tuple(jnp.int32(i) for i in start_indices),
                          static_slice_sizes)
  return _mask(out, dynamic_slice_sizes, fill_value)
