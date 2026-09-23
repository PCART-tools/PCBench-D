def pattern_match_scan_to_fori_loop(
    jaxpr: jax_core.Jaxpr, num_consts: int, num_carry: int
) -> tuple[jax_core.Jaxpr, bool]:
  if num_carry > 0:
    # Pattern match onto fori_loop:
    # We expect the first carry argument to the jaxpr to be the loop index and
    # for the loop index + 1 to be returned as the first value out of the loop.
    in_index_var = jaxpr.invars[num_consts]
    out_index_var = jaxpr.outvars[0]
    # Check that the loop index argument is an int32 scalar
    if (in_index_var.aval.shape or
        in_index_var.aval.dtype not in (jnp.int32, jnp.int64)):
      raise NotImplementedError(
          f"not a fori_loop index in: {in_index_var.aval} {jaxpr=}")
    if (out_index_var.aval.shape or
        out_index_var.aval.dtype not in (jnp.int32, jnp.int64)):
      raise NotImplementedError(
          f"not a fori_loop index out: {out_index_var.aval} {jaxpr=}")
    # Look for the equation that increments the loop index
    for i, eqn in enumerate(jaxpr.eqns):
      if eqn.primitive == lax.add_p:
        if eqn.invars[0] == in_index_var:
          if isinstance(eqn.invars[1], jax_core.Literal):
            if eqn.invars[1].val == 1:
              if eqn.outvars[0] == out_index_var:
                eqn_index = i
                break
    else:
      raise NotImplementedError("Unable to match fori_loop pattern")
    # Delete the equation that increments and remove the loop index from the
    # output. Incrementing the loop index will be done implicitly.
    jaxpr = jaxpr.replace(
        eqns=jaxpr.eqns[:eqn_index] + jaxpr.eqns[eqn_index + 1:],
        outvars=jaxpr.outvars[1:])
    has_loop_index = True
  else:
    # If there's no carry, the loop index has been DCEd and the body does *not*
    # expect a loop index as an argument.
    has_loop_index = False
  return jaxpr, has_loop_index
