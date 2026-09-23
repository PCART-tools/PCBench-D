def get_unconstrained_dims(sharding: NamedSharding):
  return {i for i, axes in enumerate(sharding._parsed_pspec)
          if axes is None}
