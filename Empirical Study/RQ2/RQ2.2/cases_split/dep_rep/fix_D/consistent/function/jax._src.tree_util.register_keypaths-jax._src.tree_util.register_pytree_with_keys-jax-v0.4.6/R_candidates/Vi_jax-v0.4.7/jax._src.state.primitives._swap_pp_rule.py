def _swap_pp_rule(eqn, context, settings) -> pp.Doc:
  y, = eqn.outvars
  x, v, *idx = eqn.invars
  idx = _pp_idx(context, idx, eqn.params["indexed_dims"])
  if type(y) is core.DropVar:
    # In the case of a set (ignored return value),
    # pretty print `_ = swap x v i` as `x[i] <- v`
    del y
    return pp.concat([
        pp_ref(pp.concat([
            pp.text(core.pp_var(x, context)),
            pp.text('['), idx, pp.text(']')
        ])), pp.text(' <- '), pp.text(core.pp_var(v, context))])
  else:
    # pretty-print `y:T = swap x v i` as `y:T, x[i] <- x[i], v`
    x_i = pp.concat([pp.text(core.pp_var(x, context)),
                     pp.text('['), idx, pp.text(']')])
    y = core.pp_vars([y], context, print_shapes=settings.print_shapes)
    return pp.concat([y, pp.text(', '), pp_ref(x_i), pp.text(' <- '),
                      pp_ref(x_i), pp.text(', '),
                      pp.text(core.pp_var(v, context))])
