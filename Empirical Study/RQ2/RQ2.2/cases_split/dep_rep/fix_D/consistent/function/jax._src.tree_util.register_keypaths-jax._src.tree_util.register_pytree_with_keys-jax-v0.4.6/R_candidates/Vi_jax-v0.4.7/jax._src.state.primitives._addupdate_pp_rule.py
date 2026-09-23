def _addupdate_pp_rule(eqn, context, settings) -> pp.Doc:
  # pretty-print ` = addupdate x i v` as `x[i] += v`
  () = eqn.outvars
  x, v, *idx = eqn.invars
  idx = _pp_idx(context, idx, eqn.params["indexed_dims"])
  return pp.concat([
    pp_ref(pp.concat([
        pp.text(core.pp_var(x, context)),
        pp.text('['), idx, pp.text(']')
    ])), pp.text(' += '), pp.text(core.pp_var(v, context))])
