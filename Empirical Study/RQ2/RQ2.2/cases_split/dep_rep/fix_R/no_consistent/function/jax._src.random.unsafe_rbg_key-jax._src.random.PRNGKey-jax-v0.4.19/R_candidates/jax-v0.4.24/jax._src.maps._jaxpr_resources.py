def _jaxpr_resources(jaxpr, resource_env) -> set[ResourceAxisName]:
  if isinstance(jaxpr, core.ClosedJaxpr):
    jaxpr = jaxpr.jaxpr
  assert isinstance(jaxpr, core.Jaxpr)
  used_resources = set()
  for eqn in jaxpr.eqns:
    if eqn.primitive is xmap_p:
      if eqn.params['resource_env'].physical_mesh != resource_env.physical_mesh:
        raise RuntimeError("Changing the physical mesh is not allowed inside xmap.")
      used_resources |= set(it.chain(*eqn.params['axis_resources'].values()))
    updates = core.traverse_jaxpr_params(
        partial(_jaxpr_resources, resource_env=resource_env), eqn.params).values()
    for update in updates:
      used_resources |= update
  return used_resources
