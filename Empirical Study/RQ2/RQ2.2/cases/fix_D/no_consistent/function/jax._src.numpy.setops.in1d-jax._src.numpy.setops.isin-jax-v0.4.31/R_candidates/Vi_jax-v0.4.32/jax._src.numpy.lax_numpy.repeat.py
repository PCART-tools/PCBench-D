def repeat(a: ArrayLike, repeats: ArrayLike, axis: int | None = None, *,
           total_repeat_length: int | None = None) -> Array:
  """Construct an array from repeated elements.

  JAX implementation of :func:`numpy.repeat`.

  Args:
    a: N-dimensional array
    repeats: 1D integer array specifying the number of repeats. Must match the
      length of the repeated axis.
    axis: integer specifying the axis of ``a`` along which to construct the
      repeated array. If None (default) then ``a`` is first flattened.
    total_repeat_length: this must be specified statically for ``jnp.repeat``
      to be compatible with :func:`~jax.jit` and other JAX transformations.
      If ``sum(repeats)`` is larger than the specified ``total_repeat_length``,
      the remaining values will be discarded. If ``sum(repeats)`` is smaller
      than ``total_repeat_length``, the final value will be repeated.

  Returns:
    an array constructed from repeated values of ``a``.

  See Also:
    - :func:`jax.numpy.tile`: repeat a full array rather than individual values.

  Examples:
    Repeat each value twice along the last axis:

    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.repeat(a, 2, axis=-1)
    Array([[1, 1, 2, 2],
           [3, 3, 4, 4]], dtype=int32)

    If ``axis`` is not specified, the input array will be flattened:

    >>> jnp.repeat(a, 2)
    Array([1, 1, 2, 2, 3, 3, 4, 4], dtype=int32)

    Pass an array to ``repeats`` to repeat each value a different number of times:

    >>> repeats = jnp.array([2, 3])
    >>> jnp.repeat(a, repeats, axis=1)
    Array([[1, 1, 2, 2, 2],
           [3, 3, 4, 4, 4]], dtype=int32)

    In order to use ``repeat`` within ``jit`` and other JAX transformations, the
    size of the output must be specified statically using ``total_repeat_length``:

    >>> jit_repeat = jax.jit(jnp.repeat, static_argnames=['axis', 'total_repeat_length'])
    >>> jit_repeat(a, repeats, axis=1, total_repeat_length=5)
    Array([[1, 1, 2, 2, 2],
           [3, 3, 4, 4, 4]], dtype=int32)

    If `total_repeat_length` is smaller than ``sum(repeats)``, the result will be truncated:

    >>> jit_repeat(a, repeats, axis=1, total_repeat_length=4)
    Array([[1, 1, 2, 2],
           [3, 3, 4, 4]], dtype=int32)

    If it is larger, then the additional entries will be filled with the final value:

    >>> jit_repeat(a, repeats, axis=1, total_repeat_length=7)
    Array([[1, 1, 2, 2, 2, 2, 2],
           [3, 3, 4, 4, 4, 4, 4]], dtype=int32)
  """
  util.check_arraylike("repeat", a)
  core.is_dim(repeats) or util.check_arraylike("repeat", repeats)

  if axis is None:
    a = ravel(a)
    axis = 0
  else:
    a = asarray(a)

  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.repeat()")
  assert isinstance(axis, int)  # to appease mypy

  if core.is_symbolic_dim(repeats):
    if total_repeat_length is not None:
      raise ValueError("jnp.repeat with a non-constant `repeats` is supported only "
                       f"when `total_repeat_length` is None. ({repeats=} {total_repeat_length=})")

  # If total_repeat_length is not given, use a default.
  if total_repeat_length is None:
    repeats = core.concrete_or_error(None, repeats,
      "When jit-compiling jnp.repeat, the total number of repeats must be static. "
      "To fix this, either specify a static value for `repeats`, or pass a static "
      "value to `total_repeat_length`.")

    # Fast path for when repeats is a scalar.
    if np.ndim(repeats) == 0 and ndim(a) != 0:
      input_shape = shape(a)
      axis = _canonicalize_axis(axis, len(input_shape))
      aux_axis = axis + 1
      aux_shape: list[DimSize] = list(input_shape)
      aux_shape.insert(aux_axis, operator.index(repeats) if core.is_constant_dim(repeats) else repeats)  # type: ignore
      a = lax.broadcast_in_dim(
        a, aux_shape, [i for i in range(len(aux_shape)) if i != aux_axis])
      result_shape: list[DimSize] = list(input_shape)
      result_shape[axis] *= repeats
      return reshape(a, result_shape)

    repeats = np.ravel(repeats)
    if ndim(a) != 0:
      repeats = np.broadcast_to(repeats, [shape(a)[axis]])
    total_repeat_length = np.sum(repeats)
  else:
    repeats = ravel(repeats)
    if ndim(a) != 0:
      repeats = broadcast_to(repeats, [shape(a)[axis]])

  # Special case when a is a scalar.
  if ndim(a) == 0:
    if shape(repeats) == (1,):
      return full([total_repeat_length], a)
    else:
      raise ValueError('`repeat` with a scalar parameter `a` is only '
      'implemented for scalar values of the parameter `repeats`.')

  # Special case if total_repeat_length is zero.
  if total_repeat_length == 0:
    result_shape = list(shape(a))
    result_shape[axis] = 0
    return reshape(array([], dtype=_dtype(a)), result_shape)

  # If repeats is on a zero sized axis, then return the array.
  if shape(a)[axis] == 0:
    return asarray(a)

  # This implementation of repeat avoid having to instantiate a large.
  # intermediate tensor.

  # Modify repeats from e.g. [1,2,0,5] -> [0,1,2,0] for exclusive repeat.
  exclusive_repeats = roll(repeats, shift=1).at[0].set(0)
  # Cumsum to get indices of new number in repeated tensor, e.g. [0, 1, 3, 3]
  scatter_indices = reductions.cumsum(exclusive_repeats)
  # Scatter these onto a zero buffer, e.g. [1,1,0,2,0,0,0,0]
  block_split_indicators = zeros([total_repeat_length], dtype=int32)
  block_split_indicators = block_split_indicators.at[scatter_indices].add(1)
  # Cumsum again to get scatter indices for repeat, e.g. [0,1,1,3,3,3,3,3]
  gather_indices = reductions.cumsum(block_split_indicators) - 1
  return take(a, gather_indices, axis=axis)
