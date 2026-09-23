def _get_shardings_from_executable(
    xla_executable, out_shardings, device_assignment, global_out_avals,
    num_ordered_effects, all_default_mem_kind
  ):
  out_shardings_xla = get_gspmd_shardings_from_executable(  # type: ignore
      xla_executable, device_assignment, len(global_out_avals),
      num_ordered_effects, all_default_mem_kind)  # type: ignore
  if out_shardings_xla is None:
    return out_shardings, (False,) * len(global_out_avals)

  orig_out_shardings = out_shardings
  out_shardings, are_out_shardings_from_xla = [], []  # type: ignore
  for xla_s, orig, aval in safe_zip(out_shardings_xla, orig_out_shardings,
                                    global_out_avals):
    if is_unspecified(orig):
      out_shardings.append(xla_s)
      are_out_shardings_from_xla.append(True)
    else:
      xla_hlo_s = xla_s._to_xla_hlo_sharding(aval.ndim)  # type: ignore
      orig_hlo_s = orig._to_xla_hlo_sharding(aval.ndim)  # type: ignore
      # MANUAL HloSharding comes from other partitioning frameworks.
      if (not dtypes.issubdtype(aval.dtype, dtypes.extended) and
          not xla_hlo_s.is_manual() and
          (not op_shardings.are_op_shardings_equal(xla_hlo_s, orig_hlo_s) or
           xla_s.memory_kind != orig.memory_kind)):  # type: ignore
        raise AssertionError(
            f"Unexpected XLA sharding override: (XLA) {xla_s} != {orig} "
            "(User sharding)")
      out_shardings.append(orig)
      are_out_shardings_from_xla.append(False)
  return out_shardings, are_out_shardings_from_xla
