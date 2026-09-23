def _get_ref_avals(grid, in_avals, in_specs, out_avals, out_specs):
  def _get_memory_space(spec):
    if spec is no_block_spec:
      return None
    return spec.memory_space
  in_ref_avals = [
      AbstractMemoryRef(aval, _get_memory_space(in_spec))
      for aval, in_spec in zip(in_avals, in_specs)
  ]
  out_ref_avals = [
      AbstractMemoryRef(aval, _get_memory_space(out_spec))
      for aval, out_spec in zip(out_avals, out_specs)
  ]
  if grid is None:
    in_specs = [None] * len(in_avals)
    out_specs = [None] * len(out_avals)
  tiled_in_ref_avals = [
      aval if in_spec is no_block_spec
      else _tile_ref(aval, in_spec.block_shape)
      for aval, in_spec in zip(in_ref_avals, in_specs)
  ]
  tiled_out_ref_avals = [
      aval if out_spec is no_block_spec
      else _tile_ref(aval, out_spec.block_shape)
      for aval, out_spec in zip(out_ref_avals, out_specs)
  ]
  return in_specs, tiled_in_ref_avals, out_specs, tiled_out_ref_avals
