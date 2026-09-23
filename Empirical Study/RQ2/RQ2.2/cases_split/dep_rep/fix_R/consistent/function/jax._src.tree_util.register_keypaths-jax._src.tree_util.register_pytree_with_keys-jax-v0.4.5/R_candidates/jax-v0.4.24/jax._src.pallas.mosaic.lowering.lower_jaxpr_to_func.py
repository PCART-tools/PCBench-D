def lower_jaxpr_to_func(
    ctx: ir.Context,
    jaxpr: jax_core.Jaxpr,
    *,
    mosaic_grid_mapping: MosaicGridMapping,
    name: str,
) -> func.FuncOp:
  num_grid = len(mosaic_grid_mapping.grid_types)
  num_scalar_prefetch = len(mosaic_grid_mapping.scalar_prefetch_types)
  arg_types = [
      *mosaic_grid_mapping.grid_types,
      *mosaic_grid_mapping.scalar_prefetch_types,
      *mosaic_grid_mapping.operand_types,
      *mosaic_grid_mapping.scratch_types,
  ]
  arg_block_shapes = [
      *mosaic_grid_mapping.scalar_prefetch_block_shapes,
      *mosaic_grid_mapping.operand_block_shapes,
      *mosaic_grid_mapping.scratch_block_shapes,
  ]
  def body_func(*args):
    grid_indices, scalar_prefetch, operands_and_scratch = split_list(
        args, [num_grid, num_scalar_prefetch])
    grid_indices = mosaic_grid_mapping.get_grid_indices(grid_indices)
    jaxpr_indices = tuple(idx for i, idx in enumerate(grid_indices)
                          if i not in mosaic_grid_mapping.mapped_dims)
    mesh_info = mosaic_grid_mapping.mesh_info
    if mesh_info is not None:
      (l_to_m,), scalar_prefetch = split_list(scalar_prefetch, [1])
      mesh_context = MeshContext(l_to_m, mesh_info.axis_names,
                                 mesh_info.mesh_strides)
    else:
      mesh_context = None
    lowering_context = LoweringContext(
        ctx,
        jaxpr_indices,
        arg_block_shapes,
        source_info_util.NameStack(),
        mesh_context=mesh_context,
        traceback_caches=mlir.TracebackCaches(),
    )
    return jaxpr_subcomp(
        lowering_context, jaxpr, *scalar_prefetch, *operands_and_scratch
    )
  body_func.__name__ = name
  body = func.FuncOp.from_py_func(*arg_types, name=name)(body_func)
  try:
    body.func_op.verify()
  except Exception as e:
    raise LoweringException(
        f"Body failed to verify: {body.func_op}.\nThis is an internal error."
        " Please report a bug at:"
        " https://github.com/google/jax/issues/new?assignees=sharadmv."
    ) from e
  return body.func_op
