def _get_pp_rule(eqn, context, settings) -> pp.Doc:
  # Pretty prints `a = get x i` as `x[i] <- a`
  y, = eqn.outvars
  x, *idx = eqn.invars
  idx = _pp_idx(context, idx, eqn.params["indexed_dims"])
  lhs = core.pp_vars([y], context, print_shapes=settings.print_shapes)
  # TODO more general get
  return pp.concat([lhs, pp.text(' <- '), pp_ref(pp.concat([
      pp.text(core.pp_var(x, context)), pp.text('['), idx, pp.text(']')]))])
