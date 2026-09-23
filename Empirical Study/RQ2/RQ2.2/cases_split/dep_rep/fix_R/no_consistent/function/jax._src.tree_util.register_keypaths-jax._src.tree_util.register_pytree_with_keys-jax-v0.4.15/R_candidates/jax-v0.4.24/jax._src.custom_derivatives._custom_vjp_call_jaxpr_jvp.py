def _custom_vjp_call_jaxpr_jvp(
    primals, tangents, *, fun_jaxpr: core.ClosedJaxpr,
    fwd_jaxpr_thunk: Callable[..., tuple[core.Jaxpr, Sequence[Any]]],
    num_consts: int, bwd: Callable, out_trees: Callable, symbolic_zeros: bool):
  _, args = split_list(primals, [num_consts])
  consts_dot, args_dot = split_list(tangents, [num_consts])
  if any(type(t) is not Zero for t in consts_dot):
    raise ad.CustomVJPException()
  zeros = [type(t) is not Zero for t in args_dot]
  fwd_jaxpr, fwd_consts = fwd_jaxpr_thunk(*zeros)  # consts can be tracers!
  _, res_tree = out_trees()
  res_and_primals_out = core.eval_jaxpr(fwd_jaxpr, fwd_consts, *args)
  res, primals_out = split_list(res_and_primals_out, [res_tree.num_leaves])
  avals_out = [raise_to_shaped(core.get_aval(x)) for x in primals_out]
  args_dot = map(ad.instantiate_zeros, args_dot)
  # Cast float0 to zeros with the primal dtype because custom vjp rules don't
  # currently handle float0s
  args_dot = map(ad.replace_float0s, args, args_dot)
  tangents_out = ad.custom_lin_p.bind(
      *res, *args_dot, num_res=res_tree.num_leaves, bwd=bwd,
      out_avals=avals_out, symbolic_zeros=symbolic_zeros)
  tangents_out = map(lax.tie_p.bind, primals_out, tangents_out)
  tangents_out = map(ad.recast_to_float0, primals_out, tangents_out)
  return primals_out, tangents_out
