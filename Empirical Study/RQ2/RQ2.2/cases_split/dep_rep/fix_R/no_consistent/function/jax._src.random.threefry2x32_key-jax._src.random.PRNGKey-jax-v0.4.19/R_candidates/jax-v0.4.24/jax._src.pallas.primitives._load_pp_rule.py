def _load_pp_rule(eqn, context, settings):
  # Pretty prints `a = load x i` as `x[i] <- a`
  y, = eqn.outvars
  x, indexers, mask, other  = tree_util.tree_unflatten(eqn.params["args_tree"],
                                                       eqn.invars)
  # TODO(sharadmv): pretty print mask and other
  lhs = jax_core.pp_vars([y], context, print_shapes=settings.print_shapes)
  result = [
      lhs,
      pp.text(' <- '),
      sp.pp_ref_indexers(context, x, indexers)
  ]
  if mask is not None:
    result += [
        pp.text(" "),
        pp.text("mask="),
        pp.text(jax_core.pp_var(mask, context)),
    ]
  if other is not None:
    result += [
        pp.text(" "),
        pp.text("other="),
        pp.text(jax_core.pp_var(other, context)),
    ]
  return pp.concat(result)
