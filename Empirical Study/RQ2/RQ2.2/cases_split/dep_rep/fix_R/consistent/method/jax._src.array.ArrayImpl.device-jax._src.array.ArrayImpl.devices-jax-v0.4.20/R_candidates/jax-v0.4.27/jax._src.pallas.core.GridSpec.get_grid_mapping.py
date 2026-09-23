  def get_grid_mapping(
      self, in_avals, in_tree, out_avals, out_tree
  ) -> tuple[tuple[jax_core.AbstractValue, ...], GridMapping]:
    flat_in_specs, flat_out_specs = self._get_in_out_specs(
        in_avals, in_tree, out_avals, out_tree)
    in_specs, in_ref_avals, out_specs, out_ref_avals = _get_ref_avals(
        self.grid, in_avals, flat_in_specs, out_avals,
        flat_out_specs)
    grid_avals = [jax_core.ShapedArray((), jnp.dtype("int32"))] * len(self.grid)
    # Create args, kwargs pytree def
    grid_tree = tree_util.tree_structure((tuple(grid_avals), {}))
    in_block_mappings = map(
        partial(_convert_block_spec_to_block_mapping, grid_avals,
                in_tree=grid_tree), in_specs, in_ref_avals)
    out_block_mappings = map(
        partial(_convert_block_spec_to_block_mapping, grid_avals,
                in_tree=grid_tree), out_specs, out_ref_avals)
    grid_mapping = GridMapping(
        self.grid, (*in_block_mappings, *out_block_mappings), (),
        num_index_operands=0, num_scratch_operands=0)
    jaxpr_in_avals = tree_util.tree_unflatten(in_tree, in_ref_avals)
    jaxpr_out_avals = tree_util.tree_unflatten(out_tree, out_ref_avals)
    if not isinstance(jaxpr_out_avals, (tuple, list)):
      jaxpr_out_avals = (jaxpr_out_avals,)
    return (*jaxpr_in_avals, *jaxpr_out_avals), grid_mapping
