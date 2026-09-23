def threefry_split(key: typing.Array, shape: Shape) -> typing.Array:
  shape = tuple(unsafe_map(core.concrete_dim_or_error, shape))
  return _threefry_split(key, shape)
