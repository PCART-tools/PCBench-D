def _scan_pp_rule(eqn, context, settings):
  printed_params = dict(eqn.params)
  del printed_params['linear']
  if eqn.params['num_consts'] + eqn.params['num_carry'] == len(eqn.invars):
    del printed_params['length']
  if printed_params['unroll'] == 1:
    del printed_params['unroll']
  if printed_params['num_carry'] == 0:
    del printed_params['num_carry']
  if printed_params['num_consts'] == 0:
    del printed_params['num_consts']
  if not printed_params['reverse']:
    del printed_params['reverse']
  return core._pp_eqn(eqn.replace(params=printed_params), context, settings)
