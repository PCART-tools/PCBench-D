def _reduce_scatter_abstract_eval(x, *, axis_name, scatter_dimension,
                                  axis_index_groups, axis_size, tiled):
  if not isinstance(axis_name, (list, tuple)):
    axis_name = (axis_name,)
  x_aval = core.raise_to_shaped(x)
  new_shape = list(x_aval.shape)
  scatter_dim_input_size = x_aval.shape[scatter_dimension]
  if tiled:
    if scatter_dim_input_size % axis_size != 0:
      raise ValueError(f"tiled reduce_scatter operand scatter dimension size "
                       f"{scatter_dim_input_size} must be divisible by "
                       f"shard_count {axis_size}")
    new_shape[scatter_dimension] = scatter_dim_input_size // axis_size
  else:
    if scatter_dim_input_size != axis_size:
      raise ValueError(f"reduce_scatter operand scatter dimension size "
                       f"{scatter_dim_input_size} must match shard count "
                       f"{axis_size}")
    del new_shape[scatter_dimension]

  new_named_shape = {
      name: size
      for name, size in x_aval.named_shape.items()
      if name not in axis_name
  }
  return x_aval.update(shape=new_shape, named_shape=new_named_shape)
