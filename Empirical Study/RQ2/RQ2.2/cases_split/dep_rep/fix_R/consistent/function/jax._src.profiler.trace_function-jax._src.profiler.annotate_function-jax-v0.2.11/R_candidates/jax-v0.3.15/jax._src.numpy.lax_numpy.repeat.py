@_wraps(np.repeat, lax_description=_TOTAL_REPEAT_LENGTH_DOC)
def repeat(a, repeats, axis: Optional[int] = None, *, total_repeat_length=None):
  _check_arraylike("repeat", a, repeats)

  if axis is None:
    a = ravel(a)
    axis = 0

  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.repeat()")
  assert isinstance(axis, int)  # to appease mypy

  # If total_repeat_length is not given, can't compile, use a default.
  if total_repeat_length is None:
    repeats = core.concrete_or_error(np.array, repeats,
      "When jit-compiling jnp.repeat, the total number of repeats must be static. "
      "To fix this, either specify a static value for `repeats`, or pass a static "
      "value to `total_repeat_length`.")

    # Fast path for when repeats is a scalar.
    if np.ndim(repeats) == 0 and ndim(a) != 0:
      input_shape = a.shape
      aux_axis = axis if axis < 0 else axis + 1
      a = expand_dims(a, aux_axis)
      reps = [1] * len(a.shape)
      reps[aux_axis] = repeats
      a = tile(a, reps)
      result_shape = list(input_shape)
      result_shape[axis] *= repeats
      return reshape(a, result_shape)

    repeats = np.ravel(repeats)
    if ndim(a) != 0:
      repeats = np.broadcast_to(repeats, [a.shape[axis]])
    total_repeat_length = np.sum(repeats)
  else:
    repeats = ravel(repeats)
    if ndim(a) != 0:
      repeats = broadcast_to(repeats, [a.shape[axis]])

  # Special case when a is a scalar.
  if ndim(a) == 0:
    if repeats.shape == (1,):
      return full([total_repeat_length], a)
    else:
      raise ValueError('`repeat` with a scalar parameter `a` is only '
      'implemented for scalar values of the parameter `repeats`.')

  # Special case if total_repeat_length is zero.
  if total_repeat_length == 0:
    result_shape = list(a.shape)
    result_shape[axis] = 0
    return reshape(array([], dtype=a.dtype), result_shape)

  # If repeats is on a zero sized axis, then return the array.
  if a.shape[axis] == 0:
    return a

  # This implementation of repeat avoid having to instantiate a large.
  # intermediate tensor.

  # Modify repeats from e.g. [1,2,0,5] -> [0,1,2,0] for exclusive repeat.
  exclusive_repeats = roll(repeats, shift=1).at[0].set(0)
  # Cumsum to get indices of new number in repeated tensor, e.g. [0, 1, 3, 3]
  scatter_indices = cumsum(exclusive_repeats)
  # Scatter these onto a zero buffer, e.g. [1,1,0,2,0,0,0,0]
  block_split_indicators = zeros([total_repeat_length], dtype=int32)
  block_split_indicators = block_split_indicators.at[scatter_indices].add(1)
  # Cumsum again to get scatter indices for repeat, e.g. [0,1,1,3,3,3,3,3]
  gather_indices = cumsum(block_split_indicators) - 1
  return take(a, gather_indices, axis=axis)
