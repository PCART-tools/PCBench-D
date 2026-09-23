def _custom_jvp_call_jaxpr_vmap(
    axis_size, axis_name, main_type, args, in_dims, *, fun_jaxpr: core.ClosedJaxpr,
    jvp_jaxpr_thunk: Callable[[], Tuple[core.Jaxpr, Sequence[Any]]],
    num_consts: int):
  args = [batching.moveaxis(x, d, 0) if d is not not_mapped and d != 0
          else x for x, d in zip(args, in_dims)]
  num_out = len(fun_jaxpr.out_avals)

  in_batched = [d is not not_mapped for d in in_dims]
  batched_fun_jaxpr, out_batched = batching.batch_jaxpr(
      fun_jaxpr, axis_size, in_batched, False, axis_name, main_type)
  out_dims1 = [0 if b else not_mapped for b in out_batched]
  out_dims2 = []  # mutable cell updated by batched_jvp_jaxpr_thunk

  @pe._memoize
  def batched_jvp_jaxpr_thunk():
    jvp_jaxpr = core.ClosedJaxpr(*jvp_jaxpr_thunk())  # consts can be tracers
    _, args_batched = split_list(in_batched, [num_consts])
    _, all_batched = batching.batch_jaxpr(jvp_jaxpr, axis_size, args_batched * 2, False,
                                          axis_name, main_type)
    primals_batched, tangents_batched = split_list(all_batched, [num_out])
    out_batched = map(op.or_, primals_batched, tangents_batched)
    out_dims2.append([0 if b else not_mapped for b in out_batched])
    batched_jvp_jaxpr, _ = batching.batch_jaxpr(
        jvp_jaxpr, axis_size, args_batched * 2, out_batched * 2,
        axis_name, main_type)
    return batched_jvp_jaxpr.jaxpr, batched_jvp_jaxpr.consts

  batched_outs = custom_jvp_call_jaxpr_p.bind(
      *args, fun_jaxpr=batched_fun_jaxpr,
      jvp_jaxpr_thunk=batched_jvp_jaxpr_thunk, num_consts=num_consts)
  out_dims = out_dims2[0] if out_dims2 else out_dims1
  return batched_outs, out_dims
