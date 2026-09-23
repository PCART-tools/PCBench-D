def threefry_split(key: jnp.ndarray, num: int) -> jnp.ndarray:
  return _threefry_split(key, int(num))  # type: ignore
