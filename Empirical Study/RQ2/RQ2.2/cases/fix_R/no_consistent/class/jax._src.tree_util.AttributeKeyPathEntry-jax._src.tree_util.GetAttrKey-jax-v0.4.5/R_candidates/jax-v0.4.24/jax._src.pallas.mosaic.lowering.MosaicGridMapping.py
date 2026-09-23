@dataclasses.dataclass(init=False)
class MosaicGridMapping:
  grid: tuple[int, ...] | None
  jaxpr: jax_core.Jaxpr
  block_mappings: tuple[pl_core.BlockMapping | None, ...]
  mapped_dims: tuple[int, ...]
  scalar_prefetch_types: tuple[ir.Type, ...]
  operand_types: tuple[ir.Type, ...]
  scratch_types: tuple[ir.Type, ...]
  grid_types: tuple[ir.Type, ...]
  scalar_prefetch_block_shapes: tuple[tuple[int, ...], ...]
  operand_block_shapes: tuple[tuple[int, ...], ...]
  scratch_block_shapes: tuple[tuple[int, ...], ...]
  mesh_info: MeshInfo | None
  get_grid_indices: Callable | None

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

  def _prepare_mesh_info(self, mesh: mesh_lib.Mesh | None):
    if not self.has_communication:
      self.mesh_info = None
      return
    if mesh is None:
      raise ValueError(
          "Cannot use communication in pallas_call without shard_map."
      )
    axis_names = mesh.axis_names
    # We need mesh <-> logical translation tables. Since the logical IDs are
    # just linearized versions of the mesh IDs, we create those tables.
    mesh_strides = pallas_utils.strides_from_shape(tuple(
        mesh.shape[a] for a in axis_names
    ))
    logical_to_mesh = np.empty((mesh.size, len(axis_names)), dtype=np.int32)
    for i, idx in enumerate(np.ndindex(*mesh.device_ids.shape)):
      logical_to_mesh[i] = np.array(idx)
    self.mesh_info = MeshInfo(logical_to_mesh, axis_names, mesh_strides)
    l_to_m_aval = pl_core.AbstractMemoryRef(
        jax_core.raise_to_shaped(jax_core.get_aval(logical_to_mesh)),
        TPUMemorySpace.SMEM,
    )
    # We are now passing in the logical -> mesh index mapping
    # TODO(sharadmv,apaszke): avoid stalling pipeline by marking the index
    # mapping as scalar prefetch and instead just mark it as an SMEM operand.
    self.scalar_prefetch_types = (
        _get_arg_type(l_to_m_aval, None)[0],
        *self.scalar_prefetch_types)

  def maybe_compress_grid(self):
    # If we have many leading parallel dimensions, we should "compress" them
    # into one so we can load balance across cores as best as we can.
    # TODO(sharadmv): implement this optimization
    pass

  @functools.cached_property
  def has_communication(self) -> bool:
    return bool(jax_core.used_axis_names_jaxpr(self.jaxpr))

  def get_extra_args(self) -> tuple[Any, ...]:
    if self.mesh_info is None:
      return ()
    return (self.mesh_info.logical_to_mesh,)

  def get_dimension_semantics(self) -> ir.ArrayAttr:

    def _get_semantics(s: str | None) -> str:
      if s is None:
        return "#tpu.dimension_semantics<arbitrary>"
      return f"#tpu.dimension_semantics<{s}>"

    return ir.ArrayAttr.get(
        map(
            ir.Attribute.parse,
            map(_get_semantics, self._dimension_semantics),
        )
    )
