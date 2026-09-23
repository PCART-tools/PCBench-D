@lru_cache(maxsize=4096)
def _process_in_axis_resources(in_shardings_thunk, in_type,
                               in_tree, resource_env):
  orig_in_shardings = in_shardings_thunk()
  # Only do this if original in_shardings are unspecified. If they are
  # FROM_GDA or AUTO, go via flatten_axis_resources.
  if _is_unspecified(orig_in_shardings):
    in_shardings_flat = (orig_in_shardings,) * len(in_type)
  else:
    in_shardings_flat = flatten_axis_resources(
          "pjit in_shardings", in_tree, orig_in_shardings,
          tupled_args=True)

  if not config.jax_dynamic_shapes:
    pjit_check_aval_sharding(in_shardings_flat, in_type,
                             "pjit arguments", allow_uneven_sharding=False)
  # TODO(yashkatariya): Only check for is_auto or _is_unspecified when
  # FROM_GDA is removed.
  canonicalized_shardings = tuple(
      i if _is_unspecified_or_from_gda_or_auto(i) else to_gspmd_sharding(i, aval.ndim)
      for i, aval in zip(in_shardings_flat, in_type))
  return canonicalized_shardings
