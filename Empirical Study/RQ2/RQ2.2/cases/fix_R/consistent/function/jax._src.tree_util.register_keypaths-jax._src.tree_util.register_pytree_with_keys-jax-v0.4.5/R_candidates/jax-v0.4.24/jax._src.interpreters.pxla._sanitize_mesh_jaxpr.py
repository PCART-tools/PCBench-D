def _sanitize_mesh_jaxpr(jaxpr):
  if isinstance(jaxpr, core.ClosedJaxpr):
    jaxpr = jaxpr.jaxpr
  for eqn in jaxpr.eqns:
    if eqn.primitive.name in _forbidden_primitives:
      raise RuntimeError(f"Nesting {_forbidden_primitives[eqn.primitive.name]} "
                         f"inside xmaps not supported!")
    core.traverse_jaxpr_params(_sanitize_mesh_jaxpr, eqn.params)
