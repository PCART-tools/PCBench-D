def _unravel_index_hlo(axis_env):
  div = mlir.ir_constant(
      np.array(axis_env.nreps // math.prod(axis_env.sizes), np.uint32))
  mod = mlir.ir_constant(np.array(axis_env.sizes[-1], np.uint32))
  return hlo.RemOp(
      hlo.DivOp(hlo.ReplicaIdOp().result, div).result, mod).result
