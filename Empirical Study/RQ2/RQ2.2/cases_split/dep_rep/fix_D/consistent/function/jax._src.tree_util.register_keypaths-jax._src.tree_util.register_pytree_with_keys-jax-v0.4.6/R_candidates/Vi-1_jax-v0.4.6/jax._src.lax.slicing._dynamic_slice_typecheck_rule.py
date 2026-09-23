def _dynamic_slice_typecheck_rule(x, *starts_and_dyn_sizes, slice_sizes):
  start_indices, dyn = util.split_list(starts_and_dyn_sizes, [x.aval.ndim])
  if not dyn:
    out_aval, effects = dynamic_slice_p.abstract_eval(
        x.aval, *(d.aval for d in start_indices), slice_sizes=slice_sizes)
    return [out_aval], effects
  else:
    # TODO(mattjj): perform more checks
    out_shape = lax._merge_dyn_shape(slice_sizes, dyn)
    out_shape = [d.val if type(d) is core.Literal else d for d in out_shape]
    out_aval = core.DShapedArray(tuple(out_shape), x.aval.dtype,
                                 x.aval.weak_type)
    return [out_aval], core.no_effects
