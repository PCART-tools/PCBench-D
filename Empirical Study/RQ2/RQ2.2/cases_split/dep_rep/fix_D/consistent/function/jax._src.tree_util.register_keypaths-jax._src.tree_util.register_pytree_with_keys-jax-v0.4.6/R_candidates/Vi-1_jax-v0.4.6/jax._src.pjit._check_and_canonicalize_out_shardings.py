@lru_cache(maxsize=4096)
def _check_and_canonicalize_out_shardings(
    out_shardings_thunk, out_tree, global_out_avals):
  orig_out_shardings = out_shardings_thunk()
  # TODO(yashkatariya): Remove the if branch and fix flatten_axis_resources
  # instead. This condition exists because flatten_axis_resources passes in an
  # `object()` while unflattening which breaks assertion is user defined
  # pytrees (which shouldn't exist but they do).
  if (_is_unspecified(orig_out_shardings) or
      isinstance(orig_out_shardings, XLACompatibleSharding)):
    out_shardings_flat = (orig_out_shardings,) * len(global_out_avals)
  else:
    out_shardings_flat = flatten_axis_resources(
        "pjit out_shardings", out_tree(), orig_out_shardings,
        tupled_args=False)

  pjit_check_aval_sharding(out_shardings_flat, global_out_avals, "pjit outputs",
                           allow_uneven_sharding=False)

  canonicalized_out_shardings_flat = tuple(
      o if _is_unspecified(o) or is_auto(o) else to_gspmd_sharding(o, aval.ndim)
      for o, aval in safe_zip(out_shardings_flat, global_out_avals)
  )
  return canonicalized_out_shardings_flat
