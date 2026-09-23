def _convert_elt_type_pp_rule(eqn, context, settings):
  # don't print new_dtype because the output binder shows it, don't print
  # weak_type when false
  params = dict(eqn.params)
  del params['new_dtype']  # output binder shows it
  if not params['weak_type']: del params['weak_type']  # don't show trivial case
  return core._pp_eqn(eqn.replace(params=params), context, settings)
