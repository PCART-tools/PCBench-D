def _swap_pp_rule(eqn, context, settings):
  # Pretty prints `a = swap x v i` as `a, x[i] <- x[i], v`
  # or:
  # Pretty prints `_ = swap x v i` as `x[i] <- v`
  y, = eqn.outvars
  x, val, *args = eqn.invars
  idx, *masked_other = tree_util.tree_unflatten(eqn.params["args_tree"], args)
  idx = _pp_idx(eqn.invars[0].aval, idx, context)
  x_i = pp.concat([pp.text(jax_core.pp_var(x, context)),
                   pp.text('['), idx, pp.text(']')])
  if isinstance(y, jax_core.DropVar):
    return pp.concat([state_primitives.pp_ref(
      x_i), pp.text(" <- "), pp.text(jax_core.pp_var(val, context))])
  y = jax_core.pp_vars([y], context, print_shapes=settings.print_shapes)
  return pp.concat([y, pp.text(', '), state_primitives.pp_ref(x_i),
                    pp.text(' <- '), state_primitives.pp_ref(x_i),
                    pp.text(', '), pp.text(jax_core.pp_var(val, context))])
