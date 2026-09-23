def _parse_input_dimensions(
    args: tuple[NDArray, ...],
    input_core_dims: list[CoreDims],
    error_context: str = "",
) -> tuple[tuple[int, ...], dict[str, int]]:
  """Parse broadcast and core dimensions for vectorize with a signature.

  Args:
    args: tuple of input arguments to examine.
    input_core_dims: list of core dimensions corresponding to each input.
    error_context: string context for error messages.

  Returns:
    broadcast_shape: common shape to broadcast all non-core dimensions to.
    dim_sizes: common sizes for named core dimensions.
  """
  if len(args) != len(input_core_dims):
    raise TypeError(
        'wrong number of positional arguments: expected %r, got %r %s'
        % (len(input_core_dims), len(args), error_context))
  shapes = []
  dim_sizes: dict[str, int] = {}
  for arg, core_dims in zip(args, input_core_dims):
    _update_dim_sizes(dim_sizes, arg.shape, core_dims, error_context,
                      is_input=True)
    ndim = arg.ndim - len(core_dims)
    shapes.append(arg.shape[:ndim])
  broadcast_shape = lax.broadcast_shapes(*shapes)
  # TODO(mattjj): this code needs updating for dynamic shapes (hence ignore)
  return broadcast_shape, dim_sizes  # type: ignore
