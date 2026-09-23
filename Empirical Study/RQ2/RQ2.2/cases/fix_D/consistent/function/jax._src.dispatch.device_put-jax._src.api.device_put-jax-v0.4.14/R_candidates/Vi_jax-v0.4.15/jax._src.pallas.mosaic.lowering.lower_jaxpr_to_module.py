def lower_jaxpr_to_module(
    ctx: ir.Context,
    grid_mapping: core.GridMapping,
    jaxpr: jax_core.Jaxpr,
    dimension_semantics: tuple[str | None, ...] | None,
    memory_spaces: tuple[TPUMemorySpace | None, ...] | None
) -> ir.Module:
  m = ir.Module.create()
  sym_tab = ir.SymbolTable(m.operation)
  if all(bm is None for bm in grid_mapping.block_mappings):
    # Trivial grid-map, we don't need to populate the transform functions.
    func_op = lower_jaxpr_to_func(ctx, jaxpr, grid_mapping=grid_mapping,
                                  memory_spaces=memory_spaces,
                                  name="main")
    m.body.append(func_op)
    sym_tab.insert(func_op)
    return m
  func_op = lower_jaxpr_to_func(ctx, jaxpr, grid_mapping=grid_mapping,
                                memory_spaces=memory_spaces,
                                name="main")
  m.body.append(func_op)
  sym_tab.insert(func_op)
  num_smem_inputs = grid_mapping.num_index_operands
  window_params = []
  grid = grid_mapping.grid
  for i, bm in enumerate(grid_mapping.block_mappings):
    func_name = f"transform_{i}"
    if bm.index_map_jaxpr.consts:
      raise NotImplementedError("Index map jaxpr with consts not supported.")
    mlir_func = lower_jaxpr_to_transform_func(
        ctx,
        bm.index_map_jaxpr.jaxpr,
        [*[None] * len(grid), *[SMEM] * num_smem_inputs],
        name=func_name)
    assert mlir_func.verify(), mlir_func
    block_shape = [
        1 if b is core.mapped else b for b in bm.block_shape
    ]
    window_shape = ir.DenseI64ArrayAttr.get(block_shape)
    window_params.append(
        ir.DictAttr.get(
            dict(
                window_bounds=window_shape,
                transform_indices=ir.FlatSymbolRefAttr.get(func_name),
            )
        )
    )
    m.body.append(mlir_func)
    sym_tab.insert(mlir_func)
  func_op.attributes["scalar_prefetch"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), num_smem_inputs)
  func_op.attributes["window_params"] = ir.ArrayAttr.get(window_params)
  func_op.attributes["iteration_bounds"] = ir.DenseI64ArrayAttr.get(
      grid_mapping.grid
  )

  def _get_semantics(s: str | None) -> str:
    if s is None:
      return "#tpu.dimension_semantics<arbitrary>"
    return f"#tpu.dimension_semantics<{s}>"

  if dimension_semantics is None:
    func_dimension_semantics = [
        _get_semantics("parallel")
        if i in grid_mapping.mapped_dims
        else _get_semantics(None)
        for i, d in enumerate(grid_mapping.grid)
    ]
  else:
    dimension_semantics_iter = iter(dimension_semantics)
    func_dimension_semantics = [
        _get_semantics("parallel")
        if i in grid_mapping.mapped_dims
        else _get_semantics(next(dimension_semantics_iter))
        for i, d in enumerate(grid_mapping.grid)
    ]
  func_op.attributes["dimension_semantics"] = ir.ArrayAttr.get(
      map(ir.Attribute.parse, func_dimension_semantics)
  )
  return m
