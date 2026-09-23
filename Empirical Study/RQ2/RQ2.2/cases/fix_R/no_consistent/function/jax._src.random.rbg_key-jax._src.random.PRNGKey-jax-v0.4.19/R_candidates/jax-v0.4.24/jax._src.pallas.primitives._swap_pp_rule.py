def _swap_pp_rule(eqn, context, settings):
  # Pretty prints `a = swap x v i` as `a, x[i] <- x[i], v`
  # or:
  # Pretty prints `_ = swap x v i` as `x[i] <- v`
  y, = eqn.outvars
  x, indexers, val, mask = eqn.params["args_tree"].unflatten(eqn.invars)
  x_i = sp.pp_ref_indexers(context, x, indexers)
  if isinstance(y, jax_core.DropVar):
    return pp.concat([
        x_i,
        pp.text(" <- "), pp.text(jax_core.pp_var(val, context))])
  y = jax_core.pp_vars([y], context, print_shapes=settings.print_shapes)
  result = [
      y,
      pp.text(", "),
      x_i,
      pp.text(" <- "),
      x_i,
      pp.text(", "),
      pp.text(jax_core.pp_var(val, context)),
  ]
  if mask is not None:
    result += [
        pp.text(" "),
        pp.text("mask="),
        pp.text(jax_core.pp_var(mask, context)),
    ]
  return pp.concat(result)
