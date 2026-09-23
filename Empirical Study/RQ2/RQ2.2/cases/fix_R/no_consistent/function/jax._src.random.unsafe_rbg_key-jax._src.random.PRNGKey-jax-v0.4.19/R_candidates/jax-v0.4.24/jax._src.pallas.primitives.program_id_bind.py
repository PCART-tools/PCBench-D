def program_id_bind(*, axis: int):
  grid_env = pallas_core.current_grid_env()
  if grid_env:
    return grid_env[axis].axis_index
  return jax_core.Primitive.bind(program_id_p, axis=axis)
