@contextlib.contextmanager
def grid_env(env: tuple[tuple[Any, int], ...]) -> Iterator[None]:
  _grid_env_stack.append(tuple(GridEnv(axis_index, axis_size)
                               for axis_index, axis_size in env))
  try:
    yield
  finally:
    _grid_env_stack.pop()
