def _get_ref_avals(grid, in_avals, in_specs, out_avals, out_specs):
  if grid is None:
    in_specs = [None] * len(in_avals)
    out_specs = [None] * len(out_avals)
    in_ref_avals = [state.shaped_array_ref(arg.shape, arg.dtype)
                    for arg in in_avals]
    out_ref_avals = [state.shaped_array_ref(arg.shape, arg.dtype)
                     for arg in out_avals]
  else:
    in_ref_avals = [
        state.shaped_array_ref(
            _compute_shape_from_block_spec(
                block_spec, arg.shape), arg.dtype)
        for block_spec, arg in zip(in_specs, in_avals)]
    out_ref_avals = [
        state.shaped_array_ref(
            _compute_shape_from_block_spec(
                block_spec, arg.shape), arg.dtype)
        for block_spec, arg in zip(out_specs, out_avals)]
  return in_specs, in_ref_avals, out_specs, out_ref_avals
