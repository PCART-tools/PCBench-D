def _get_normalized_avals_and_shardings(
    global_in_avals: Sequence[ShapedArray],
    in_shardings: Sequence[sharding_internal.XLACompatibleSharding], in_is_global: Sequence[bool]
) -> Tuple[Sequence[ShapedArray], Sequence[sharding_internal.XLACompatibleSharding]]:
  avals = []
  shardings = []

  for gaval, i, is_global in safe_zip(global_in_avals, in_shardings,
                                      in_is_global):
    if is_global:
      aval = gaval
      in_sharding = i
    else:
      assert isinstance(i, sharding_internal.NamedSharding)
      aval = i.mesh._global_to_local(
          cast(ArrayMapping, get_array_mapping(i.spec)), gaval)  # pylint: disable=g-bare-generic
      in_sharding = sharding_internal.NamedSharding(i.mesh.local_mesh, i.spec)
    avals.append(aval)
    shardings.append(in_sharding)

  return avals, shardings
