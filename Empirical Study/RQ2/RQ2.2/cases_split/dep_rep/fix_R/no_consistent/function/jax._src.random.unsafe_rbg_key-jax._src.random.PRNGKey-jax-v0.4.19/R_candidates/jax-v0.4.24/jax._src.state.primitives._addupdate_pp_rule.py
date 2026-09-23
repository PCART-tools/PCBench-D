def _addupdate_pp_rule(eqn, context, settings) -> pp.Doc:
  del settings
  # pretty-print ` = addupdate x i v` as `x[i] += v`
  () = eqn.outvars
  x, v, *flat_idx = eqn.invars
  indexers = tree_util.tree_unflatten(eqn.params["tree"], flat_idx)
  return pp.concat([
    pp_ref_indexers(context, x, indexers),
    pp.text(' += '),
    pp.text(core.pp_var(v, context))])
