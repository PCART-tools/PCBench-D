def pjit_error_check(error, enabled_errors, *vals_in, jaxpr,
                     in_shardings, out_shardings, resource_env,
                     donated_invars, name,
                     in_positional_semantics, out_positional_semantics,
                     inline, keep_unused):
  # jaxpr to checked_jaxpr
  err_vals, err_tree = jtu.tree_flatten(error)
  new_vals_in = [*err_vals, *vals_in]
  in_avals = tuple(map(get_shaped_aval, new_vals_in))
  checked_jaxpr, out_tree, _ = jaxpr_to_checkify_jaxpr(jaxpr, enabled_errors,
                                                       err_tree, *in_avals)

  # Update pjit params to account for extra error values.
  num_error_vals = len(err_vals)
  num_out_error_vals = out_tree.num_leaves - len(out_shardings)
  if jax.config.jax_array:
    sharding = pjit._UNSPECIFIED
  else:
    sharding = GSPMDSharding.get_replicated(
        list(resource_env.physical_mesh.devices.flat))

  new_in_shardings = (*[sharding] * num_error_vals, *in_shardings)
  new_out_shardings = (*[sharding] * num_out_error_vals, *out_shardings)

  pos_sem = (maps._PositionalSemantics.GLOBAL if jax.config.jax_array
             else maps._positional_semantics.val)
  if not isinstance(in_positional_semantics, Iterable):
    in_positional_semantics = (in_positional_semantics,)
  if not isinstance(out_positional_semantics, Iterable):
    out_positional_semantics = (out_positional_semantics,)
  new_positional_sems_in = (*[pos_sem] * num_error_vals,
                            *in_positional_semantics)
  new_positional_sems_out = (*[pos_sem] * num_error_vals,
                             *out_positional_semantics)
  new_donated_invars = (*[False] * num_error_vals, *donated_invars)

  err_and_out = pjit.pjit_p.bind(
      *new_vals_in,
      jaxpr=checked_jaxpr,
      in_shardings=new_in_shardings,
      out_shardings=new_out_shardings,
      resource_env=resource_env,
      donated_invars=new_donated_invars,
      name=name,
      in_positional_semantics=new_positional_sems_in,
      out_positional_semantics=new_positional_sems_out,
      inline=inline,
      keep_unused=keep_unused,
  )
  return tree_unflatten(out_tree, err_and_out)
