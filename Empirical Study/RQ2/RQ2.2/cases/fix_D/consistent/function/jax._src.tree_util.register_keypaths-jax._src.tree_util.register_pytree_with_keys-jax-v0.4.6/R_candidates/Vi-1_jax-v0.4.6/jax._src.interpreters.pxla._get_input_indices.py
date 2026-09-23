def _get_input_indices(
    avals: Sequence[ShapedArray], shardings: Sequence[sharding_internal.XLACompatibleSharding]
) -> Sequence[Tuple[Optional[Index], ...]]:

  input_indices = []
  for aval, sharding in zip(avals, shardings):
    if aval is core.abstract_token:
      index = tuple(
          (slice(None),) for _ in range(len(sharding.addressable_devices)))
    else:
      # We special case this logic to support fully replicated values because
      # the mesh is global mesh and the indices returned by `spec_to_indices` will
      # represent index for each device in the global mesh. But here we want
      # indices for the local devices of the global mesh.
      proto = sharding._to_xla_op_sharding(aval.ndim)
      if is_op_sharding_replicated(proto):
        index = tuple(
            (slice(None),) * aval.ndim
            for _ in range(len(sharding.addressable_devices)))  # type: ignore
      else:
        index = tuple(
            sharding.addressable_devices_indices_map(
                aval.shape).values())  # type: ignore
    input_indices.append(index)

  return input_indices
