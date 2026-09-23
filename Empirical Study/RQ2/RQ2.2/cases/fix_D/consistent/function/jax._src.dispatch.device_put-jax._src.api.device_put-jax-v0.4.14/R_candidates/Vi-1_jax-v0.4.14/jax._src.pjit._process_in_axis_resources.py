@lru_cache(maxsize=4096)
def _process_in_axis_resources(in_shardings_thunk, in_avals, in_tree,
                               resource_env, debug_info, device_or_backend_set):
  orig_in_shardings = in_shardings_thunk()
  # Only do this if original in_shardings are unspecified. If it is AUTO, go
  # via flatten_axis_resources.
  if is_unspecified(orig_in_shardings):
    in_shardings_flat = (orig_in_shardings,) * len(in_avals)
  else:
    in_shardings_flat = flatten_axis_resources(
          "pjit in_shardings", in_tree, orig_in_shardings,
          tupled_args=True)

  if not config.jax_dynamic_shapes:
    pjit_check_aval_sharding(in_shardings_flat, in_avals,
                             None if debug_info is None else debug_info.arg_names,
                             "pjit arguments", allow_uneven_sharding=False)
  canonicalized_shardings = tuple(
      i if is_unspecified_or_auto(i) else
      to_gspmd_sharding(i, aval.ndim, device_or_backend_set)
      for i, aval in zip(in_shardings_flat, in_avals))
  return canonicalized_shardings
