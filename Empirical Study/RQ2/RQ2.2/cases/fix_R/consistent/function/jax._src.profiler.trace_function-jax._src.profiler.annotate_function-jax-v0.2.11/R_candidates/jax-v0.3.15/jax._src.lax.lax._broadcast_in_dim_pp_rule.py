def _broadcast_in_dim_pp_rule(eqn, context, settings):
  # Don't print shape or trivial broadcast_dimensions in params, since it can be
  # inferred from the let-binder's type annotation.
  printed_params = {}
  if eqn.params['broadcast_dimensions']:
    printed_params['broadcast_dimensions'] = eqn.params['broadcast_dimensions']
  lhs = core.pp_vars(eqn.outvars, context, print_shapes=settings.print_shapes)
  rhs = [pp.text(eqn.primitive.name),
         core.pp_kv_pairs(sorted(printed_params.items()), context, settings),
         pp.text(" ") + core.pp_vars(eqn.invars[:1], context)]
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  return [lhs, pp.text(" = ", annotation=annotation), *rhs]
