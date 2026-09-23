@lru_cache(maxsize=4096)
def _process_in_axis_resources(in_shardings_thunk, local_in_avals,
                               in_tree, in_positional_semantics, is_gda,
                               resource_env):
  orig_in_shardings = in_shardings_thunk()
  # Only do this if original in_shardings are unspecified. If they are
  # FROM_GDA or AUTO, go via flatten_axis_resources.
  if _is_unspecified(orig_in_shardings):
    in_shardings_flat = (orig_in_shardings,) * len(local_in_avals)
  else:
    in_shardings_flat = flatten_axis_resources(
          "pjit in_shardings", in_tree, orig_in_shardings,
          tupled_args=True)

  # Fork here because the `Array` path is very simple and doesn't need all the
  # complexity below.
  if config.jax_array:
    pjit_check_aval_sharding(in_shardings_flat, local_in_avals, "pjit arguments",
                             allow_uneven_sharding=False)
    global_in_avals = local_in_avals
    # TODO(yashkatariya): Only check for is_auto or _is_unspecified when
    # FROM_GDA is removed.
    canonicalized_shardings = tuple(
        i if _is_unspecified_or_from_gda_or_auto(i) else to_gspmd_sharding(i, aval.ndim)
        for i, aval in safe_zip(in_shardings_flat, global_in_avals))
    return tuple(global_in_avals), canonicalized_shardings

  if not local_in_avals:
    assert not in_shardings_flat
    return (), ()

  in_axis_resources_flat = tuple(
      i if _is_from_gda(i) or is_auto(i) else i._parsed_pspec
      for i in in_shardings_flat)

  # This check should be above local_to_global call below otherwise if
  # `FROM_GDA` is passed to any input other than GDA, a ugly error message
  # will be raised because get_array_mapping (in local_to_global) of a
  # FROM_GDA cannot happen.
  tree_map(_check_resources_mismatch, in_axis_resources_flat, is_gda)
  # If all inputs have global semantics or fully replicated, then the avals are
  # global and the mesh should also be global. This split is because
  # non-contiguous mesh can only be used if all inputs have global semantics or
  # fully replicated.
  # Use canonicalized in_axis_resources here because we want to treat P(None)
  # and None (for example) as equivalent.
  if all(
      (not _is_from_gda(p) and not is_auto(p) and
       CanonicalizedParsedPartitionSpec(p).partitions == ()) or
      ips == pxla._PositionalSemantics.GLOBAL
      for p, ips in safe_zip(in_axis_resources_flat, in_positional_semantics)):
    # Shapes should be checked against non canonicalized in_axis_resources.
    # For example, partitions of () and ((),) are not equivalent, since the
    # first one is a valid spec for a scalar value, while the second is not!
    pjit_check_aval_sharding(in_shardings_flat, local_in_avals, "pjit arguments",
                             allow_uneven_sharding=False)
  else:
    pjit_check_aval_sharding(
        [i if _is_from_gda(i) or is_auto(i) else
         NamedSharding(i.mesh.local_mesh, i.spec)
         for i in in_shardings_flat],
        local_in_avals, "pjit arguments", allow_uneven_sharding=False)

  # Local or global avals doesn't matter for converting to op sharding because
  # the `ndim` does not change.
  canonicalized_in_shardings_flat = tuple(
      i if _is_from_gda(i) or is_auto(i) else to_gspmd_sharding(i, aval.ndim)
      for i, aval in safe_zip(in_shardings_flat, local_in_avals))

  global_in_avals = local_to_global(
      in_positional_semantics, local_in_avals, canonicalized_in_shardings_flat,
      resource_env.physical_mesh)

  return tuple(global_in_avals), canonicalized_in_shardings_flat
