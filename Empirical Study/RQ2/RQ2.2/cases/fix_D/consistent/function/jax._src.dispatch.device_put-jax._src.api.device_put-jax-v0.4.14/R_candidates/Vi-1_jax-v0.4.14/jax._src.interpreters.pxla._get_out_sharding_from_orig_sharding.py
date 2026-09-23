def _get_out_sharding_from_orig_sharding(
    out_shardings, out_avals, orig_s, orig_aval, are_out_sharding_from_xla):
  out = []
  orig_handler = _orig_out_sharding_handlers[type(orig_s)]
  for o, out_aval, from_xla in safe_zip(out_shardings, out_avals,
                                        are_out_sharding_from_xla):
    if isinstance(o, sharding_impls.GSPMDSharding):
      try:
        # Only return the same input sharding object if the OpShardings and
        # in_aval.ndim and out_aval.ndim match. This is because if OpSharding is
        # replicated then, it doesn't encode the ndim in it. The devices
        # will be the same at this point because those checks happen before.
        if (orig_aval is not None and out_aval is not None and
            out_aval.ndim == orig_aval.ndim and
            sharding_impls.are_op_shardings_equal(
                o._hlo_sharding, orig_s._to_xla_hlo_sharding(orig_aval.ndim))):
          out.append((orig_s, False))
        else:
          out.append((orig_handler(o._hlo_sharding, orig_s), False))
      except:
        out.append((o, from_xla))
    else:
      out.append((o, from_xla))
  return out
