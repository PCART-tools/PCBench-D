def remat_vmap(spmd_axis_name, axis_size, axis_name, main_type, args, dims, *,
               jaxpr, **params):
  assert not jaxpr.constvars
  jaxpr_batched_, out_batched = batching.batch_jaxpr_axes(
      pe.close_jaxpr(jaxpr), axis_size, dims,
      [batching.zero_if_mapped] * len(jaxpr.outvars),
      axis_name=axis_name, spmd_axis_name=spmd_axis_name, main_type=main_type)
  jaxpr_batched, consts = jaxpr_batched_.jaxpr, jaxpr_batched_.consts
  if consts:
    jaxpr_batched = pe.convert_constvars_jaxpr(jaxpr_batched)
  out_dims = [0 if b else None for b in out_batched]
  return remat_p.bind(*consts, *args, jaxpr=jaxpr_batched, **params), out_dims
