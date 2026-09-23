def _process_grid_to_3d_grid(builder, grid_mapping: GridMapping):
  if len(grid_mapping.grid) <= 3:
    program_ids = [
        tl.program_id(axis=i, _builder=builder)
        for i in range(len(grid_mapping.grid))
    ]
    return grid_mapping.grid, program_ids
  grid_prefix = grid_mapping.grid[:-2]
  grid_suffix = grid_mapping.grid[-2:]
  total_axis_size = np.prod(grid_prefix)
  new_grid = (total_axis_size, *grid_suffix)
  out_indices = [0] * len(grid_prefix)
  grid0 = tl.program_id(0, _builder=builder)
  for i, s in reversed(list(enumerate(grid_prefix))):
    grid0, out_indices[i] = (
        grid0.__floordiv__(s, _builder=builder),
        grid0.__mod__(s, _builder=builder),
    )
  out_indices = [
      *out_indices,
      tl.program_id(1, _builder=builder),
      tl.program_id(2, _builder=builder),
  ]
  assert len(out_indices) == len(grid_mapping.grid)
  return new_grid, out_indices
