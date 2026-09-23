def lower_jaxpr_to_func(
    ctx: ir.Context,
    jaxpr: jax_core.Jaxpr,
    *,
    memory_spaces: Sequence[tpu_core.TPUMemorySpace | None] | None,
    grid_mapping: core.GridMapping | None,
    name: str,
) -> func.FuncOp:
  if grid_mapping:
    arg_types = map(
        aval_to_ir_type,
        [jax_core.ShapedArray((), jnp.int32) for _ in grid_mapping.grid],
    )
  else:
    arg_types = []

  def _get_arg_type(aval, block_mapping: core.BlockMapping | None,
                    memory_space: tpu_core.TPUMemorySpace | None):
    if block_mapping is None:
      return aval_to_ir_type(aval, memory_space=memory_space), aval.shape
    shape = tuple(
        1 if b is core.mapped else b for b in block_mapping.block_shape
    )
    return (aval_to_ir_type(aval, shape=shape, memory_space=memory_space),
            block_mapping.block_shape)
  if memory_spaces is None:
    memory_spaces = [None] * len(jaxpr.invars)
  if len(memory_spaces) != len(jaxpr.invars):
    raise ValueError("Must have as many memory spaces as inputs and outputs.")
  if grid_mapping is None:
    block_mappings = [None] * len(jaxpr.invars)
  else:
    scalar_prefetch = grid_mapping.num_index_operands
    block_mappings = grid_mapping.block_mappings
    block_mappings = [*[None] * scalar_prefetch, *block_mappings]
    for memory_space in memory_spaces[:scalar_prefetch]:
      if memory_space is not None and memory_space != SMEM:
        raise ValueError("Cannot specify non-SMEM memory space for "
                         "scalar prefetch inputs.")
    memory_spaces = memory_spaces[scalar_prefetch:]
    memory_spaces = [*[SMEM] * scalar_prefetch, *memory_spaces]
  invar_arg_types, block_shapes = unzip2(
      map(_get_arg_type, [invar.aval for invar in jaxpr.invars], block_mappings,
          memory_spaces)
  )
  arg_types = [*arg_types, *invar_arg_types]
  if grid_mapping:

    def body_func(*args):
      grid_indices, args = split_list(args, [len(grid_mapping.grid)])
      grid_indices = [
          g
          for i, g in enumerate(grid_indices)
          if i not in grid_mapping.mapped_dims
      ]
      lowering_context = LoweringContext(
          ctx,
          grid_mapping,
          tuple(grid_indices),
          block_shapes,
          source_info_util.NameStack(),
      )
      return jaxpr_subcomp(lowering_context, jaxpr, *args)

  else:
    lowering_context = LoweringContext(
        ctx, None, None, block_shapes, source_info_util.NameStack()
    )
    body_func = functools.partial(jaxpr_subcomp, lowering_context, jaxpr)
  body_func.__name__ = name
  body = func.FuncOp.from_py_func(*arg_types, name=name)(body_func)
  body.func_op.verify()
  return body.func_op
