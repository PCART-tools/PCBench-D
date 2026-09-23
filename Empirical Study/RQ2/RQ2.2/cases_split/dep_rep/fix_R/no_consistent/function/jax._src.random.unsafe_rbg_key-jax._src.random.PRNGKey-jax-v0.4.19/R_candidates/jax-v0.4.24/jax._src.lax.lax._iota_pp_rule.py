def _iota_pp_rule(eqn, context, settings):
  printed_params = {}
  if len(eqn.params['shape']) > 1:
    printed_params['dimension'] = eqn.params['dimension']
  return core._pp_eqn(eqn.replace(params=printed_params), context, settings)
