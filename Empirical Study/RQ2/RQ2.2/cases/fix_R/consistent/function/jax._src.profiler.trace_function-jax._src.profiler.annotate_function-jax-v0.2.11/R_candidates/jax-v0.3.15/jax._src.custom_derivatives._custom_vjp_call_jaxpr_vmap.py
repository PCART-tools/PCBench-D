def _custom_vjp_call_jaxpr_vmap(
    axis_size, axis_name, main_type, args, in_dims, *, fun_jaxpr: core.ClosedJaxpr,
    fwd_jaxpr_thunk: Callable[[], Tuple[core.Jaxpr, Sequence[Any]]],
    bwd: lu.WrappedFun, out_trees: Callable, num_consts: int):
  args = [batching.moveaxis(x, d, 0) if d is not not_mapped and d != 0
          else x for x, d in zip(args, in_dims)]

  in_batched = [d is not not_mapped for d in in_dims]
  _, args_batched = split_list(in_batched, [num_consts])
  batched_fun_jaxpr, out_batched = batching.batch_jaxpr(
      fun_jaxpr, axis_size, in_batched, False, axis_name, main_type)
  out_dims1 = [0 if b else not_mapped for b in out_batched]
  out_dims2 = []

  @pe._memoize
  def batched_fwd_jaxpr_thunk():
    fwd_jaxpr = core.ClosedJaxpr(*fwd_jaxpr_thunk())  # consts can be tracers
    batched_fwd_jaxpr, out_batched = batching.batch_jaxpr(
        fwd_jaxpr, axis_size, args_batched, False, axis_name, main_type)
    out_dims2.append([0 if b else not_mapped for b in out_batched])
    return batched_fwd_jaxpr.jaxpr, batched_fwd_jaxpr.consts

  fwd_args_batched = [0 if b else not_mapped for b in args_batched]
  fwd_out_dims = lambda: out_dims2[0]
  batched_bwd = batching.batch_custom_vjp_bwd(bwd, axis_name, axis_size, fwd_out_dims,
                                              fwd_args_batched, main_type)

  batched_outs = custom_vjp_call_jaxpr_p.bind(
      *args, fun_jaxpr=batched_fun_jaxpr,
      fwd_jaxpr_thunk=batched_fwd_jaxpr_thunk, bwd=batched_bwd,
      out_trees=out_trees, num_consts=num_consts)
  out_dims = out_dims2[0] if out_dims2 else out_dims1
  return batched_outs, out_dims
