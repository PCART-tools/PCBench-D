def _convert_elt_type_pp_rule(eqn, context, settings):
  # don't print new_dtype because the output binder shows it, don't print
  # weak_type when false
  printed_params = {}
  if eqn.params['weak_type']:
    printed_params['weak_type'] = True
  lhs = core.pp_vars(eqn.outvars, context, print_shapes=settings.print_shapes)
  rhs = [pp.text(eqn.primitive.name),
         core.pp_kv_pairs(sorted(printed_params.items()), context, settings),
         pp.text(" ") + core.pp_vars(eqn.invars, context)]
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  return [lhs, pp.text(" = ", annotation=annotation), *rhs]
