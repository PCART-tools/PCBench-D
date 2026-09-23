def _prepare_jit(fun, static_argnums, static_argnames, donate_argnums,
                 args, kwargs):
  # Validate donate_argnums
  if max(donate_argnums, default=-1) >= len(args):
    raise ValueError(
        f"jitted function has donate_argnums={donate_argnums} but "
        f"was called with only {len(args)} positional arguments.")

  f = lu.wrap_init(fun)
  f, args = argnums_partial_except(f, static_argnums, args, allow_invalid=True)
  f, kwargs = argnames_partial_except(f, static_argnames, kwargs)
  args_flat, in_tree = tree_flatten((args, kwargs))
  if donate_argnums:
    donated_invars = donation_vector(donate_argnums, args, kwargs)
  else:
    donated_invars = (False,) * len(args_flat)

  return f, in_tree, args_flat, donated_invars
