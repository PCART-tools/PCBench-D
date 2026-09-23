def _pjit_pp_rule(eqn, context, settings):
  params = dict(eqn.params)
  del params['inline']
  if not any(params['donated_invars']):
    del params['donated_invars']
  if all(is_unspecified(s) for s in params['in_shardings']):
    del params['in_shardings']
  if all(is_unspecified(s) for s in params['out_shardings']):
    del params['out_shardings']
  if not params['keep_unused']:
    del params['keep_unused']
  if (params['resource_env'] is None or
      params['resource_env'].physical_mesh.empty):
    del params['resource_env']

  # Move name= to the front to make the resulting equation easier to scan.
  del params["name"]
  return core._pp_eqn(eqn, context, settings, params=["name"] + sorted(params))
