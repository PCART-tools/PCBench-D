def _get_pp_rule(eqn, context, settings) -> pp.Doc:
  # Pretty prints `a = get x i` as `x[i] <- a`
  y, = eqn.outvars
  x, *flat_idx = eqn.invars
  indexers = tree_util.tree_unflatten(eqn.params["tree"], flat_idx)
  lhs = core.pp_vars([y], context, print_shapes=settings.print_shapes)
  return pp.concat([
      lhs,
      pp.text(' <- '),
      pp_ref_indexers(context, x, indexers)
  ])
