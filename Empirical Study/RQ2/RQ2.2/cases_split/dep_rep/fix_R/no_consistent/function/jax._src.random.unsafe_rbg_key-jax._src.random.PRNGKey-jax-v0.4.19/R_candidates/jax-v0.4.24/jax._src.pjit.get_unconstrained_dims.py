def get_unconstrained_dims(sharding: NamedSharding):
  assert sharding._parsed_pspec is not None
  return {i for i, axes in enumerate(sharding._parsed_pspec)
          if axes is None}
