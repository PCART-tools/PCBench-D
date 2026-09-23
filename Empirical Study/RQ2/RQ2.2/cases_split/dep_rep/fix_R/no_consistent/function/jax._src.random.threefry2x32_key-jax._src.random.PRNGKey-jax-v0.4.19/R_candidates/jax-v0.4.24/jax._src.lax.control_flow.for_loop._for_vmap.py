def _for_vmap(spmd_axis_name, axis_size, axis_name, main_type, args, dims, *,
              jaxpr, nsteps, reverse, which_linear, unroll):
  init_batched = [d is not batching.not_mapped for d in dims]
  closed_jaxpr = _cached_for_jaxpr(jaxpr)
  batched = init_batched
  for _ in range(len(batched)):
    _, out_batched = batching.batch_jaxpr(
        closed_jaxpr,
        axis_size, [False] + batched, instantiate=batched,
        axis_name=axis_name, spmd_axis_name=spmd_axis_name, main_type=main_type)
    if out_batched == batched:
      break
    batched = map(operator.or_, batched, out_batched)
  else:
    raise Exception("Invalid fixpoint")
  args = [batching.broadcast(x, axis_size, 0) if now_bat and not was_bat
          else batching.moveaxis(x, d, 0) if now_bat else x
          for x, d, was_bat, now_bat in zip(args, dims, init_batched, batched)]
  batched_jaxpr_, _ = batching.batch_jaxpr(
      pe.close_jaxpr(jaxpr), axis_size, [False] + batched, [],
      axis_name=axis_name, spmd_axis_name=spmd_axis_name, main_type=main_type)
  batched_jaxpr, () = batched_jaxpr_.jaxpr, batched_jaxpr_.consts  # TODO consts
  out_flat = for_p.bind(*args, jaxpr=batched_jaxpr, nsteps=nsteps,
                        reverse=reverse, which_linear=which_linear,
                        unroll=unroll)
  return out_flat, [0 if b else batching.not_mapped for b in batched]
