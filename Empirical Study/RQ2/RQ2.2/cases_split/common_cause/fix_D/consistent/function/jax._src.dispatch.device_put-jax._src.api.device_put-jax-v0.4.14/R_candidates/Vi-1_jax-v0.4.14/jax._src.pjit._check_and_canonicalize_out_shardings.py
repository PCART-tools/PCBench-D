@lru_cache(maxsize=4096)
def _check_and_canonicalize_out_shardings(
    out_shardings_thunk, out_tree, out_type, debug_info, device_or_backend_set):
  orig_out_shardings = out_shardings_thunk()
  # TODO(yashkatariya): Remove the if branch and fix flatten_axis_resources
  # instead. This condition exists because flatten_axis_resources passes in an
  # `object()` while unflattening which breaks assertion is user defined
  # pytrees (which shouldn't exist but they do).
  if (is_unspecified(orig_out_shardings) or
      isinstance(orig_out_shardings, XLACompatibleSharding)):
    out_shardings_flat = (orig_out_shardings,) * len(out_type)
  else:
    out_shardings_flat = flatten_axis_resources(
        "pjit out_shardings", out_tree(), orig_out_shardings,
        tupled_args=False)

  if not config.jax_dynamic_shapes:
    pjit_check_aval_sharding(
        out_shardings_flat, out_type,
        None if debug_info is None else debug_info.result_paths,
        "pjit outputs", allow_uneven_sharding=False)

  canonicalized_out_shardings_flat = tuple(
      o if is_unspecified(o) or is_auto(o) else
      to_gspmd_sharding(o, aval.ndim, device_or_backend_set)
      for o, aval in zip(out_shardings_flat, out_type)
  )
  return canonicalized_out_shardings_flat
