def _build_axis_index_lowering_mhlo(axis_name, axis_env):
  if isinstance(axis_name, tuple):
    assert axis_name, 'empty axis name'
    if len(axis_name) > 1:
      raise NotImplementedError(
          '`axis_index` translation rule does not support multiple axis names.')
    axis_name, = axis_name
  axis_pos = list(axis_env.names).index(axis_name)
  nreplicas = axis_env.nreps // prod(axis_env.sizes)
  div = mlir.ir_constant(np.array(nreplicas * prod(axis_env.sizes[axis_pos+1:]),
                                  dtype=np.uint32))
  mod = mlir.ir_constant(np.array(axis_env.sizes[axis_pos], dtype=np.uint32))
  unsigned_index = mhlo.RemOp(mhlo.DivOp(mhlo.ReplicaIdOp(), div), mod)
  return mhlo.ConvertOp(
      ir.RankedTensorType.get([], ir.IntegerType.get_signless(32)),
      unsigned_index).result
