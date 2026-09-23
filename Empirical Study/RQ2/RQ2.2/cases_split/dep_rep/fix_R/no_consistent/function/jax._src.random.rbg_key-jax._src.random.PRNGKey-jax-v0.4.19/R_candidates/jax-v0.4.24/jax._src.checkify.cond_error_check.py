def cond_error_check(error: Error, enabled_errors, index, *ops, branches, linear):
  # Get the error-effects out of all branches so the cond can be called with
  # a merged error with all these effects.
  err_vals, err_tree = jtu.tree_flatten(error)
  in_avals = map(get_shaped_aval, [*err_vals, *ops])
  def get_error_effects_from_jaxpr(jxpr):
    _, _, effects = jaxpr_to_checkify_jaxpr(jxpr, enabled_errors, err_tree,
                                            *in_avals)
    return effects
  effects = [get_error_effects_from_jaxpr(jxpr) for jxpr in branches]
  merged_error = error._add_placeholder_effects(set().union(*effects))
  err_vals, err_tree = jtu.tree_flatten(merged_error)
  new_linear = (*[False] * len(err_vals), *linear)

  # Update branch jaxprs to be checkified jaxprs.
  in_avals = map(get_shaped_aval, [*err_vals, *ops])
  new_branches, out_trees, _ = unzip3(
      jaxpr_to_checkify_jaxpr(
          jxpr, enabled_errors, err_tree, *in_avals) for jxpr in branches)

  err_and_outs = lax.cond_p.bind(
      index, *err_vals, *ops,
      branches=tuple(new_branches), linear=new_linear)

  # we need to merge metadata across out_trees (a tuple)
  err0, out = tree_unflatten(out_trees[0], err_and_outs)
  merged_metadata = err0._metadata
  for tr in out_trees[1:]:
    err, _ = tree_unflatten(tr, err_and_outs)
    merged_metadata = {**merged_metadata, **err._metadata}
  return err0._replace(_metadata=merged_metadata), out
