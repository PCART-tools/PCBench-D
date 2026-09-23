def _update_dim_sizes(
    dim_sizes: Dict[str, int],
    shape: Tuple[int, ...],
    core_dims: CoreDims,
    error_context: str = "",
    *,
    is_input: bool):
  """Incrementally check and update core dimension sizes for a single argument.

  Args:
    dim_sizes: sizes of existing core dimensions. Will be updated in-place.
    shape: shape of this argument.
    core_dims: core dimensions for this argument.
    error_context: string context for error messages.
    is_input: are we parsing input or output arguments?
  """
  num_core_dims = len(core_dims)
  if is_input:
    if len(shape) < num_core_dims:
      raise ValueError(
          'input with shape %r does not have enough dimensions for all core '
          'dimensions %r %s' % (shape, core_dims, error_context))
  else:
    if len(shape) != num_core_dims:
      raise ValueError(
          'output shape %r does not match core dimensions %r %s'
          % (shape, core_dims, error_context))

  core_shape = shape[-num_core_dims:] if core_dims else ()
  for dim, size in zip(core_dims, core_shape):
    if dim not in dim_sizes:
      dim_sizes[dim] = size
    elif size != dim_sizes[dim]:
      raise ValueError(
          'inconsistent size for core dimension %r: %r vs %r %s'
          % (dim, size, dim_sizes[dim], error_context))
