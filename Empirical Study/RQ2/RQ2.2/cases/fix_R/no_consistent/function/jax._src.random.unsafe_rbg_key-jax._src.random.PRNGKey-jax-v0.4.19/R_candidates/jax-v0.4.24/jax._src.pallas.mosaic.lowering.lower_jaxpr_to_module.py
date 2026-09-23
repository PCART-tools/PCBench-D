def lower_jaxpr_to_module(
    ctx: ir.Context,
    grid_mapping: pl_core.GridMapping,
    in_shapes: tuple[jax.ShapeDtypeStruct, ...],
    out_shapes: tuple[jax.ShapeDtypeStruct, ...],
    jaxpr: jax_core.Jaxpr,
    dimension_semantics: tuple[str | None, ...] | None,
    mesh: mesh_lib.Mesh | None = None
) -> ir.Module:
  mosaic_grid_mapping = MosaicGridMapping(
      jaxpr, grid_mapping, dimension_semantics, mesh)
  mosaic_grid_mapping.maybe_compress_grid()
  m = ir.Module.create()
  sym_tab = ir.SymbolTable(m.operation)
  func_op = lower_jaxpr_to_func(ctx, jaxpr, mosaic_grid_mapping=mosaic_grid_mapping,
                                name="main")
  m.body.append(func_op)
  sym_tab.insert(func_op)
  window_params = []
  grid = mosaic_grid_mapping.grid
  if grid:
    invars = jaxpr.invars
    if grid_mapping.num_scratch_operands > 0:
      invars = invars[
          grid_mapping.num_index_operands:-grid_mapping.num_scratch_operands]
    else:
      invars = invars[grid_mapping.num_index_operands:]
    avals = tuple(v.aval for v in invars)
    block_operand_shapes = (
        *in_shapes[grid_mapping.num_index_operands :],
        *out_shapes,
    )
    assert len(block_operand_shapes) == len(grid_mapping.block_mappings)
    for i, (full_ty, bm, aval) in enumerate(
        zip(block_operand_shapes, grid_mapping.block_mappings, avals)
    ):
      func_name = f"transform_{i}"
      if bm is None:
        raise NotImplementedError(
            "BlockSpecs are required on TPU when grid is specified"
        )
      if bm.index_map_jaxpr.consts:
        raise NotImplementedError("Index map jaxpr with consts not supported.")
      # ANY operands don't support windowing and require empty window_params.
      if aval.memory_space == tpu_core.TPUMemorySpace.ANY:
        requires_windowing = bm.block_shape != full_ty.shape
        for atom in bm.index_map_jaxpr.jaxpr.outvars:
          if requires_windowing:
            break
          requires_windowing = not (
              isinstance(atom, jax_core.Literal) and atom.val == 0
          )
        if requires_windowing:
          raise NotImplementedError(
              "Operands in placed in the TPUMemorySpace.ANY memory space don't"
              " support windowing (i.e. non-trivial block_shape or index_map)."
          )
        window_params.append(ir.DictAttr.get())
        continue
      mlir_func = lower_jaxpr_to_transform_func(
          ctx,
          bm.index_map_jaxpr.jaxpr,
          name=func_name,
          mosaic_grid_mapping=mosaic_grid_mapping,
      )
      assert mlir_func.verify(), mlir_func
      block_shape = [
          1 if b is pl_core.mapped else b for b in bm.block_shape
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
    func_op.attributes["window_params"] = ir.ArrayAttr.get(window_params)
    static_grid = [MLIR_DYNAMIC if b is None else b for b in grid]
    func_op.attributes["iteration_bounds"] = ir.DenseI64ArrayAttr.get(static_grid)

  func_op.attributes["scalar_prefetch"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), len(mosaic_grid_mapping.scalar_prefetch_types))
  func_op.attributes["scratch_operands"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), len(mosaic_grid_mapping.scratch_types))
  func_op.attributes["dimension_semantics"] = (
      mosaic_grid_mapping.get_dimension_semantics()
  )
  return m, mosaic_grid_mapping.get_extra_args()
