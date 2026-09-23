@dataclasses.dataclass(init=False, unsafe_hash=True)
class GridSpec:
  grid: Grid
  in_specs: tuple[BlockSpec | NoBlockSpec, ...]
  out_specs: tuple[BlockSpec | NoBlockSpec, ...]
  in_specs_tree: Any
  out_specs_tree: Any

  def __init__(
      self,
      grid: Grid | None = None,
      in_specs: BlockSpec
      | Sequence[BlockSpec | NoBlockSpec]
      | NoBlockSpec = no_block_spec,
      out_specs: BlockSpec
      | Sequence[BlockSpec | NoBlockSpec]
      | NoBlockSpec = no_block_spec,
  ):
    # Be more lenient for in/out_specs
    if isinstance(in_specs, list):
      in_specs = tuple(in_specs)
    if isinstance(out_specs, list):
      out_specs = tuple(out_specs)

    self.grid = _preprocess_grid(grid)
    if in_specs is not no_block_spec:
      flat_in_specs, self.in_specs_tree = tree_util.tree_flatten(in_specs)
      self.in_specs = tuple(flat_in_specs)
    else:
      self.in_specs = in_specs
      self.in_specs_tree = None
    if out_specs is not no_block_spec:
      flat_out_specs, self.out_specs_tree = tree_util.tree_flatten(out_specs)
      self.out_specs = tuple(flat_out_specs)
    else:
      self.out_specs = out_specs
      self.out_specs_tree = None

  def _get_in_out_specs(self, in_avals, in_tree, out_avals, out_tree):
    if self.in_specs is no_block_spec:
      flat_in_specs = [no_block_spec] * len(in_avals)
    else:
      flat_in_specs = self.in_specs
      if self.in_specs_tree != in_tree:
        raise ValueError(
            "Pytree specs for arguments and `in_specs` must match: "
            f"{in_tree} vs. {self.in_specs_tree}")
    if self.out_specs is no_block_spec:
      flat_out_specs = [no_block_spec] * len(out_avals)
    else:
      flat_out_specs = self.out_specs
      if self.out_specs_tree != out_tree:
        raise ValueError(
            "Pytree specs for `out_shape` and `out_specs` must match: "
            f"{out_tree} vs. {self.out_specs_tree}")
    return flat_in_specs, flat_out_specs

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

  def unzip_dynamic_grid_bounds(self) -> tuple[GridSpec, tuple[Any, ...]]:
    static_grid = tuple(d if isinstance(d, int) else None for d in self.grid)
    dynamic_bounds = tuple(d for d in self.grid if not isinstance(d, int))
    # We can't use dataclasses.replace, because our fields are incompatible
    # with __init__'s signature.
    static_self = copy.copy(self)
    static_self.grid = static_grid
    return static_self, dynamic_bounds
