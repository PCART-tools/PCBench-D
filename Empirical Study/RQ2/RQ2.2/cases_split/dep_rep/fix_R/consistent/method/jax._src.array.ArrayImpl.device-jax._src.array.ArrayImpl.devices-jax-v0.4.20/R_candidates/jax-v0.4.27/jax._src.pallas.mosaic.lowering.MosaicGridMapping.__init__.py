  def __init__(self, jaxpr: jax_core.Jaxpr, grid_mapping: pl_core.GridMapping,
               dimension_semantics: tuple[str, ...] | None,
               mesh: mesh_lib.Mesh | None):
    self.grid = grid_mapping.grid
    self.jaxpr = jaxpr
    self.block_mappings = grid_mapping.block_mappings
    self.mapped_dims = grid_mapping.mapped_dims
    num_scalar_prefetch = grid_mapping.num_index_operands
    num_scratch = grid_mapping.num_scratch_operands
    # jaxpr has signature [*scalar_prefetch, *in_ops *out_ops, *scratch]
    num_operands = (
        len(self.jaxpr.invars)
        - num_scalar_prefetch
        - num_scratch
    )
    user_grid = tuple(
        g for i, g in enumerate(self.grid) if i not in self.mapped_dims
    )
    if dimension_semantics is None:
      dimension_semantics = ("arbitrary",) * len(user_grid)
    if len(user_grid) != len(dimension_semantics):
      raise ValueError(
          "Must have dimension semantics for each dimension of the grid."
      )
    if num_operands != len(self.block_mappings):
      raise ValueError("Must have block mappings for each operand.")
    assert len(self.mapped_dims) + len(dimension_semantics) == len(
        self.grid
    ), (
        f"Misconfigured grid: {self.mapped_dims=}, {dimension_semantics=},"
        f" {self.grid=}"
    )
    # dimension_semantics is user provided and won't take into account vmap
    # dimensions. Here we add in parallel dimensions for the vmaps.
    semantics_iter = iter(dimension_semantics)
    self._dimension_semantics = tuple(
        next(semantics_iter) if i not in self.mapped_dims else "parallel"
        for i in range(len(self.grid))
    )

    in_avals = [invar.aval for invar in self.jaxpr.invars]
    scalar_prefetch_avals, operand_avals, scratch_avals = split_list(
        in_avals, [num_scalar_prefetch, num_operands]
    )
    self.scalar_prefetch_types, _ = unzip2([
        _get_arg_type(aval, None)
        for aval in scalar_prefetch_avals])
    self.scalar_prefetch_block_shapes = tuple(
        aval.shape for aval in scalar_prefetch_avals)
    self.operand_types, self.operand_block_shapes = unzip2([
        _get_arg_type(aval, block_mapping)
        for aval, block_mapping in zip(operand_avals, self.block_mappings)])
    self.scratch_types, _ = unzip2([
        _get_arg_type(aval, None) for aval in scratch_avals])
    self.scratch_block_shapes = tuple(
        aval.shape if not isinstance(aval, tpu_core.AbstractSemaphore) else None
        for aval in scratch_avals
    )
    self.grid_types, _ = unzip2([
        _get_arg_type(jax_core.ShapedArray((), jnp.int32), None)
        for _ in range(len(self.grid))
    ])
    self._prepare_mesh_info(mesh)
    def _get_grid_indices(indices):
      return indices
    self.get_grid_indices = _get_grid_indices
