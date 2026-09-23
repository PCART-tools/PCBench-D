def _build_axis_index_lowering_hlo(ctx, axis_name, axis_env):
  if isinstance(axis_name, tuple):
    assert axis_name, 'empty axis name'
    if len(axis_name) > 1:
      raise NotImplementedError(
          '`axis_index` translation rule does not support multiple axis names.')
    axis_name, = axis_name
  axis_pos = list(axis_env.names).index(axis_name)
  nreplicas = axis_env.nreps // math.prod(axis_env.sizes)
  div = mlir.ir_constant(
      np.array(
          nreplicas * math.prod(axis_env.sizes[axis_pos + 1 :]), dtype=np.uint32
      )
  )
  mod = mlir.ir_constant(np.array(axis_env.sizes[axis_pos], dtype=np.uint32))
  axis_context = ctx.module_context.axis_context
  is_spmd = isinstance(
      axis_context,
      (sharding_impls.SPMDAxisContext, sharding_impls.ShardingContext),
  )
  if is_spmd:
    device_id = hlo.partition_id()
  else:
    device_id = hlo.replica_id()
  unsigned_index = hlo.remainder(hlo.divide(device_id, div), mod)
  return hlo.convert(
      ir.RankedTensorType.get([], ir.IntegerType.get_signless(32)),
      unsigned_index)
