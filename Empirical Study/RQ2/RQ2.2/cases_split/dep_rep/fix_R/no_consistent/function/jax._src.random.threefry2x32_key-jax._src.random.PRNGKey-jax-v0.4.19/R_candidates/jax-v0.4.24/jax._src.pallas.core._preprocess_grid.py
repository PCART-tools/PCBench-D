def _preprocess_grid(grid: Grid | int | None) -> Grid:
  if grid is None:
    return ()
  if isinstance(grid, int):
    return (grid,)
  return grid
