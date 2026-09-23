def _batch_jaxpr(closed_jaxpr, axis_size, in_batched, instantiate, axis_name,
                 spmd_axis_name, main_type):
  assert (isinstance(instantiate, bool) or
          isinstance(instantiate, (list, tuple)) and
          all(isinstance(b, bool) for b in instantiate))
  if isinstance(instantiate, bool):
    instantiate = [instantiate] * len(closed_jaxpr.out_avals)
  in_axes = [0 if b else not_mapped for b in in_batched]
  out_axes_dest = [0 if inst else zero_if_mapped for inst in instantiate]
  return batch_jaxpr_axes(closed_jaxpr, axis_size, in_axes, out_axes_dest,
                          axis_name, spmd_axis_name, main_type)
