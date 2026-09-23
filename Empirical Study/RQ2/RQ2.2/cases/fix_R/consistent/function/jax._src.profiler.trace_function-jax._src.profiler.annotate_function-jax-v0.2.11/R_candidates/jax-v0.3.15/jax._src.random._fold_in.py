def _fold_in(key: KeyArray, data: int) -> KeyArray:
  # Alternative to fold_in() to use within random samplers.
  # TODO(frostig): remove and use fold_in() once we always enable_custom_prng
  return key._fold_in(jnp.uint32(data))
