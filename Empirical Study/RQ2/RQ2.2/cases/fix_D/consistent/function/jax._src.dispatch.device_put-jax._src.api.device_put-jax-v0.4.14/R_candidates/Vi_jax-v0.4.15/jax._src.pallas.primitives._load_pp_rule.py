def _load_pp_rule(eqn, context, settings):
  # Pretty prints `a = load x i` as `x[i] <- a`
  y, = eqn.outvars
  x, *args = eqn.invars
  idx, *masked_other = tree_util.tree_unflatten(eqn.params["args_tree"], args)
  idx = _pp_idx(eqn.invars[0].aval, idx, context)
  lhs = jax_core.pp_vars([y], context, print_shapes=settings.print_shapes)
  return pp.concat([lhs, pp.text(' <- '), state_primitives.pp_ref(pp.concat([
    pp.text(jax_core.pp_var(x, context)), pp.text('['), idx, pp.text(']')
    ]))])
