def _process_grid_to_3d_grid(grid_mapping: GridMapping):
  launch_grid = []
  launch_grid_to_pallas_grid = []

  # Preserve grid order provided to pallas_call
  for i, s in enumerate(grid_mapping.grid):
    if i not in grid_mapping.mapped_dims:
      launch_grid.append(s)
      launch_grid_to_pallas_grid.append(i)

  # For mapped dims, iterate from inner to outer. This follows the pallas_call
  # batching rule that prepends the vmapped dimension.
  for dim in reversed(grid_mapping.mapped_dims):
    s = grid_mapping.grid[dim]
    launch_grid.append(s)
    launch_grid_to_pallas_grid.append(dim)

  num_collapse = len(launch_grid[:-2])

  cuda_yz_limit = 2**16 - 1

  # Check Z and then Y launch dims to make sure they're within CUDA bounds
  if (num_collapse + 1 < len(launch_grid) and
      launch_grid[num_collapse + 1] > cuda_yz_limit):
    num_collapse += 2
  elif (num_collapse < len(launch_grid) and
        launch_grid[num_collapse] > cuda_yz_limit):
    num_collapse += 1

  collapse_dims = launch_grid[:num_collapse]
  prog_id_dims = launch_grid[num_collapse:]

  if len(collapse_dims) == 0:
    prog_ids = [None] * len(prog_id_dims)
    for i in range(len(prog_id_dims)):
      out_idx = launch_grid_to_pallas_grid[i]
      prog_ids[out_idx] = tc.program_id(i)

    return prog_id_dims, prog_ids
  else:
    new_grid = [np.prod(collapse_dims), *prog_id_dims]

  assert new_grid[0] < 2**31 - 1, \
          "Cannot fix pallas kernel launch grid within CUDA limits"

  out_indices = [None] * len(grid_mapping.grid)

  grid0 = tc.program_id(0)
  for i, s in enumerate(collapse_dims):
    out_idx = launch_grid_to_pallas_grid[i]
    s = tc._to_tensor(s, grid0.dtype)
    out_indices[out_idx] = tc.semantic.mod(grid0, s)
    grid0 = tc.semantic.floordiv(grid0, s)

  for i in range(len(prog_id_dims)):
    out_idx = launch_grid_to_pallas_grid[num_collapse + i]
    out_indices[out_idx] = tc.program_id(i + 1)

  assert len(out_indices) == len(grid_mapping.grid)
  return new_grid, out_indices
