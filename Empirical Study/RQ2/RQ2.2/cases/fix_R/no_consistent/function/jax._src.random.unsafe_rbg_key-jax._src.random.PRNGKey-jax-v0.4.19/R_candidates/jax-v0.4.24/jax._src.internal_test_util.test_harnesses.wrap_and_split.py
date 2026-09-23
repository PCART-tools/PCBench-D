def wrap_and_split():
  key = jax.random.key(42)
  result = jax.random.split(key, 2)
  return jax.random.key_data(result)
