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
