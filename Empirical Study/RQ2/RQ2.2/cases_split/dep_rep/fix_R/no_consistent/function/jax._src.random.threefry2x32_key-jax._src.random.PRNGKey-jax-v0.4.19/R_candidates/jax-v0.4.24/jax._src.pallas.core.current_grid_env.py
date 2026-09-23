def current_grid_env() -> tuple[GridEnv, ...] | None:
  if not _grid_env_stack:
    return None
  return _grid_env_stack[-1]
