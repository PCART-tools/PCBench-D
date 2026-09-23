def lower_jaxpr_to_transform_func(
    ctx: ir.Context,
    jaxpr: jax_core.Jaxpr,
    *,
    name: str,
    mosaic_grid_mapping: MosaicGridMapping,
) -> func.FuncOp:
  num_grid = len(mosaic_grid_mapping.grid_types)
  arg_types = [
      *mosaic_grid_mapping.grid_types,
      *mosaic_grid_mapping.scalar_prefetch_types,
  ]
  def body_func(*args):
    grid_indices, scalar_prefetch = split_list(args, [num_grid])
    jaxpr_indices = mosaic_grid_mapping.get_grid_indices(grid_indices)
    arg_block_shapes = [
        *[()] * len(jaxpr_indices),
        *mosaic_grid_mapping.scalar_prefetch_block_shapes,
    ]

    mesh_info = mosaic_grid_mapping.mesh_info
    if mesh_info is not None:
      (l_to_m,), scalar_prefetch = split_list(scalar_prefetch, [1])
      mesh_context = MeshContext(l_to_m, mesh_info.axis_names,
                                 mesh_info.mesh_strides)
    else:
      mesh_context = None
    lowering_context = LoweringContext(
        ctx,
        None,
        arg_block_shapes,
        source_info_util.NameStack(),
        mesh_context=mesh_context,
        traceback_caches=mlir.TracebackCaches(),
    )
    return jaxpr_subcomp(lowering_context, jaxpr, *jaxpr_indices,
                         *scalar_prefetch)
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
