def _dot_general_pp_rule(eqn, context, settings):
  # suppress printing precision or preferred_element_type when None.
  # print dimension_numbers as list-of-lists to be shorter.
  printed_params = {k: v for k, v in eqn.params.items() if v is not None}
  (lhs_cont, rhs_cont), (lhs_batch, rhs_batch) = eqn.params['dimension_numbers']
  printed_params['dimension_numbers'] = (
      (list(lhs_cont), list(rhs_cont)), (list(lhs_batch), list(rhs_batch)))
  lhs = core.pp_vars(eqn.outvars, context, print_shapes=settings.print_shapes)
  rhs = [pp.text(eqn.primitive.name),
         core.pp_kv_pairs(sorted(printed_params.items()), context, settings),
         pp.text(" ") + core.pp_vars(eqn.invars, context)]
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  return [lhs, pp.text(" = ", annotation=annotation), *rhs]
