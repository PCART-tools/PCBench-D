def maybe_get_orig_out_sharding(
    in_shardings, out_shardings, are_out_shardings_from_xla, in_avals,
    out_avals):
  if all(hasattr(o, '_original_sharding') for o in out_shardings):
    return ([o._original_sharding for o in out_shardings],
            (False,) * len(out_shardings))

  orig_s = None
  orig_aval = None
  for i, aval in safe_zip(in_shardings, in_avals):
    oi = getattr(i, '_original_sharding', None)
    if type(oi) in _orig_out_sharding_handlers:
      orig_s = oi
      orig_aval = aval
      break
  if orig_s is not None:
    return zip(*_get_out_sharding_from_orig_sharding(
        out_shardings, out_avals, orig_s, orig_aval, are_out_shardings_from_xla))

  return out_shardings, are_out_shardings_from_xla
