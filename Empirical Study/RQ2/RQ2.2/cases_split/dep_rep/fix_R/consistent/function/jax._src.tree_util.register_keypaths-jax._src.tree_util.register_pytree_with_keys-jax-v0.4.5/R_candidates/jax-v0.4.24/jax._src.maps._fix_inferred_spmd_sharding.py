def _fix_inferred_spmd_sharding(jaxpr, resource_env, gen_fresh_name = None):
  rec = lambda jaxpr: _fix_inferred_spmd_sharding(jaxpr, resource_env, gen_fresh_name)
  if isinstance(jaxpr, core.ClosedJaxpr):
    return jaxpr.map_jaxpr(rec)
  assert isinstance(jaxpr, core.Jaxpr)
  if gen_fresh_name is None:
    gen_fresh_name = core.gensym([jaxpr])
  new_eqns = []
  for eqn in jaxpr.eqns:
    new_jaxpr_params = core.traverse_jaxpr_params(rec, eqn.params)
    tmp_outvars = [gen_fresh_name(v.aval) for v in eqn.outvars]
    new_eqns.append(eqn.replace(
      outvars=tmp_outvars, params=dict(eqn.params, **new_jaxpr_params)))
    for outvar, tmpvar in zip(eqn.outvars, tmp_outvars):
      mps = NamedSharding._from_parsed_pspec(
          resource_env.physical_mesh, ParsedPartitionSpec((), ()))
      unconstrained_dims = get_unconstrained_dims(mps)
      gspmd_sharding = GSPMDSharding.get_replicated(mps._device_assignment)
      new_eqns.append(core.JaxprEqn(
          [tmpvar], [outvar], sharding_constraint_p,
          dict(resource_env=resource_env,
               sharding=gspmd_sharding,
               unconstrained_dims=unconstrained_dims),
          set(),
          eqn.source_info))
  return jaxpr.replace(eqns=new_eqns)
