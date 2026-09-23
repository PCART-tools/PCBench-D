def _reshape_shape_rule(operand, *, new_sizes, dimensions):
  if not all(d >= 0 for d in new_sizes):
    msg = 'reshape new_sizes must all be positive, got {}.'
    raise TypeError(msg.format(new_sizes))
  # TODO(necula): re-enable this check
  if (not config.jax_dynamic_shapes and
      not math.prod(np.shape(operand)) == math.prod(new_sizes)):
    msg = 'reshape total size must be unchanged, got new_sizes {} for shape {}.'
    raise TypeError(msg.format(new_sizes, np.shape(operand)))
  if dimensions is not None:
    if set(dimensions) != set(range(np.ndim(operand))):
      msg = ('reshape dimensions must be a permutation of operand dimensions, '
             'got dimensions {} for shape {}.')
      raise TypeError(msg.format(dimensions, np.shape(operand)))
  return tuple(new_sizes)
