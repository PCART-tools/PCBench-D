@dataclasses.dataclass(init=False, unsafe_hash=True)
class PrefetchScalarGridSpec(pallas_core.GridSpec):
  grid: Grid
  num_scalar_prefetch: int
  in_specs: tuple[BlockSpec | NoBlockSpec, ...]
  out_specs: tuple[BlockSpec | NoBlockSpec, ...]
  in_specs_tree: Any
  out_specs_tree: Any
  scratch_shapes: tuple[Any, ...]

  def __init__(
      self,
      num_scalar_prefetch: int,
      grid: Grid | None = None,
      in_specs: BlockSpec
      | Sequence[BlockSpec | NoBlockSpec]
      | NoBlockSpec = no_block_spec,
      out_specs: BlockSpec
      | Sequence[BlockSpec | NoBlockSpec]
      | NoBlockSpec = no_block_spec,
      scratch_shapes: Any | Sequence[Any] = ()
  ):
    super().__init__(grid, in_specs, out_specs)
    self.num_scalar_prefetch = num_scalar_prefetch
    self.scratch_shapes = tuple(scratch_shapes)

  def get_grid_mapping(
      self, in_avals, in_tree, out_avals, out_tree
  ) -> tuple[tuple[jax_core.AbstractValue, ...], GridMapping]:
    all_avals = tree_util.tree_unflatten(in_tree, in_avals)
    flat_scratch_shapes, scratch_tree = tree_util.tree_flatten(
        self.scratch_shapes)
    flat_scratch_avals = map(_make_aval, flat_scratch_shapes)
    scalar_avals, unflat_in_avals = split_list(
        all_avals, [self.num_scalar_prefetch])
    flat_scalar_avals, scalar_tree = tree_util.tree_flatten(scalar_avals)
    num_flat_scalar_prefetch = len(flat_scalar_avals)
    in_avals, in_avals_tree = tree_util.tree_flatten(tuple(unflat_in_avals))
    flat_in_specs, flat_out_specs = self._get_in_out_specs(
        in_avals, in_avals_tree, out_avals, out_tree)
    in_specs, in_ref_avals, out_specs, out_ref_avals = (
        pallas_core._get_ref_avals(
            self.grid, in_avals, flat_in_specs,
            out_avals, flat_out_specs))
    scalar_ref_avals = [
        AbstractMemoryRef(jax_core.ShapedArray(aval.shape, aval.dtype),
                          TPUMemorySpace.SMEM)
        for aval in flat_scalar_avals]
    grid_avals = [jax_core.ShapedArray((), jnp.dtype("int32"))] * len(self.grid)
    # Create args, kwargs pytree def
    index_map_in_tree = tree_util.tree_structure(
        ((*grid_avals, *scalar_avals), {})
    )
    in_block_mappings = map(
        partial(_convert_block_spec_to_block_mapping,
                (*grid_avals, *scalar_ref_avals),
                in_tree=index_map_in_tree), in_specs, in_ref_avals)
    out_block_mappings = map(
        partial(_convert_block_spec_to_block_mapping,
                (*grid_avals, *scalar_ref_avals),
                in_tree=index_map_in_tree), out_specs, out_ref_avals)
    grid_mapping = GridMapping(
        grid=self.grid,
        block_mappings=(*in_block_mappings, *out_block_mappings),
        mapped_dims=(),
        num_index_operands=num_flat_scalar_prefetch,
        num_scratch_operands=len(flat_scratch_avals)
    )
    jaxpr_scalar_ref_avals = tree_util.tree_unflatten(
        scalar_tree, scalar_ref_avals)
    jaxpr_in_ref_avals = tree_util.tree_unflatten(in_avals_tree, in_ref_avals)
    jaxpr_scratch_avals = tree_util.tree_unflatten(
        scratch_tree, flat_scratch_avals)
    if not isinstance(jaxpr_scratch_avals, (tuple, list)):
      jaxpr_scratch_avals = (jaxpr_scratch_avals,)
    jaxpr_in_avals = (*jaxpr_scalar_ref_avals,
                      *jaxpr_in_ref_avals)
    jaxpr_out_avals = tree_util.tree_unflatten(out_tree, out_ref_avals)
    if not isinstance(jaxpr_out_avals, (tuple, list)):
      jaxpr_out_avals = (jaxpr_out_avals,)
    return (*jaxpr_in_avals, *jaxpr_out_avals,
            *jaxpr_scratch_avals), grid_mapping
