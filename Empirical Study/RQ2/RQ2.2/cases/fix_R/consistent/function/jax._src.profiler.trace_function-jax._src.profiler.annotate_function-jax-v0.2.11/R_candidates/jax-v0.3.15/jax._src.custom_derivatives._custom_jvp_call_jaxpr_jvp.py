def _custom_jvp_call_jaxpr_jvp(
    primals, tangents, *, fun_jaxpr: core.ClosedJaxpr,
    jvp_jaxpr_thunk: Callable[[], Tuple[core.Jaxpr, Sequence[Any]]],
    num_consts: int):
  _, args = split_list(primals, [num_consts])
  consts_dot, args_dot = split_list(tangents, [num_consts])
  if any(type(t) is not Zero for t in consts_dot):
    raise ad.CustomJVPException()
  jvp_jaxpr, jvp_consts = jvp_jaxpr_thunk()  # consts can be tracers!
  args_dot = map(ad.instantiate_zeros, args_dot)
  # Cast float0 to zeros with the primal dtype because custom jvp rules don't
  # currently handle float0s
  args_dot = map(ad.replace_float0s, args, args_dot)
  outs = core.eval_jaxpr(jvp_jaxpr, jvp_consts, *args, *args_dot)
  primals_out, tangents_out = split_list(outs, [len(outs) // 2])
  tangents_out = map(ad.recast_to_float0, primals_out, tangents_out)
  if config.jax_enable_checks:
    assert all(map(core.typecheck, fun_jaxpr.out_avals, primals_out))
  return primals_out, tangents_out
