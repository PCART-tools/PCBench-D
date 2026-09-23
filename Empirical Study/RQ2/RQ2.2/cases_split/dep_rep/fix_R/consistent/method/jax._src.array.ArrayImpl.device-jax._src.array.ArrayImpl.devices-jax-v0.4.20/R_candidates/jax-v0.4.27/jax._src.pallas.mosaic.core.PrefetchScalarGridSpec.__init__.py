  def __init__(
      self,
      num_scalar_prefetch: int,
      grid: Grid | None = None,
      in_specs: BlockSpecTree = no_block_spec,
      out_specs: BlockSpecTree = no_block_spec,
      scratch_shapes: Any | Sequence[Any] = ()
  ):
    super().__init__(grid, in_specs, out_specs)
    self.num_scalar_prefetch = num_scalar_prefetch
    self.scratch_shapes = tuple(scratch_shapes)
