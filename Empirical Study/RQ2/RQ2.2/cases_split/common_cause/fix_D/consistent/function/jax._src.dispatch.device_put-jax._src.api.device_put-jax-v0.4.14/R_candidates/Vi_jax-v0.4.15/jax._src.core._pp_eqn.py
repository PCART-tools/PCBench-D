def _pp_eqn(eqn, context, settings) -> pp.Doc:
  annotation = (source_info_util.summarize(eqn.source_info)
                if settings.source_info else None)
  name_stack_annotation = f'[{eqn.source_info.name_stack}]' if settings.name_stack else None
  lhs = pp_vars(eqn.outvars, context, print_shapes=settings.print_shapes)
  rhs = [pp.text(eqn.primitive.name, annotation=name_stack_annotation),
         pp_kv_pairs(sorted(eqn.params.items()), context, settings),
         pp.text(" ") + pp_vars(eqn.invars, context)]
  return pp.concat([lhs, pp.text(" = ", annotation=annotation), *rhs])
