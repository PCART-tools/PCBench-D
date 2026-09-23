def pjit_check_aval_sharding(
    shardings, flat_avals, names: tuple[str, ...] | None,
    what_aval: str, allow_uneven_sharding: bool):
  new_names = [''] * len(shardings) if names is None else names
  for aval, s, name in zip(flat_avals, shardings, new_names):
    if is_unspecified_or_auto(s):
      continue
    s = getattr(s, '_original_sharding', s)
    name_str = f' with pytree key path {name}' if name else ''
    shape = aval.shape
    try:
      # Sharding interfaces can implement `is_compatible_aval` as an optional
      # method to raise a more meaningful error.
      if hasattr(s, 'is_compatible_aval'):
        s.is_compatible_aval(shape)
      else:
        s._to_xla_hlo_sharding(len(shape))
    except ValueError as e:
      raise ValueError(
          f'One of {what_aval}{name_str} is incompatible with its sharding '
          f'annotation {s}: {e}')
    # Use the `OpSharding` proto to find out how many ways each dimension of
    # the aval is sharded. This approach will work across all
    # XLACompatibleSharding.
    hlo_sharding = s._to_xla_hlo_sharding(len(shape))
    assert hlo_sharding is not None
    num_ways_dim_sharded, _ = op_shardings.get_num_ways_dim_sharded(hlo_sharding)
    for i, size in enumerate(num_ways_dim_sharded):
      if not allow_uneven_sharding and shape[i] % size != 0:
        raise ValueError(f"One of {what_aval}{name_str} was given the sharding "
                         f"of {s}, which implies that "
                         f"the global size of its dimension {i} should be "
                         f"divisible by {size}, but it is equal to {shape[i]} "
                         f"(full shape: {shape})")
