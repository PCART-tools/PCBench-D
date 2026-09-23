def _broadcast_in_dim_pp_rule(eqn, context, settings):
  # Don't print shape or trivial broadcast_dimensions in params, since it can be
  # inferred from the let-binder's type annotation.
  printed_params = {}
  if eqn.params['broadcast_dimensions']:
    printed_params['broadcast_dimensions'] = eqn.params['broadcast_dimensions']
  new_eqn = eqn.replpace(params=printed_params, invars=eqn.invars[:1])
  return core._pp_eqn(new_eqn, context, settings)
