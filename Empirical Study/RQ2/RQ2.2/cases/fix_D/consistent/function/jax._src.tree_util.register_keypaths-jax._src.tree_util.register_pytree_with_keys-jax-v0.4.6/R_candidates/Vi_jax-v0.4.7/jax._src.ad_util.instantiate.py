def instantiate(z: Union[Zero, Array]) -> Array:
  if type(z) is Zero:
    return zeros_like_aval(z.aval)
  return cast(Array, z)
