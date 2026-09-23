def _extend_axis_env(env: sharding_impls.AxisEnv, name, size: int):
  return sharding_impls.AxisEnv(env.nreps, env.names + (name,),
                                env.sizes + (size,))
