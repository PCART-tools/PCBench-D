@partial(jit, static_argnums=(1,))
def _threefry_split(key, shape) -> typing.Array:
  if config.threefry_partitionable.value:
    return _threefry_split_foldlike(key, shape)  # type: ignore
  else:
    return _threefry_split_original(key, shape)  # type: ignore
