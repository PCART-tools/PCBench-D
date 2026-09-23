def _program_id_impl(*, axis: int):
  grid_env = pallas_core.current_grid_env()
  return grid_env[axis].axis_index
