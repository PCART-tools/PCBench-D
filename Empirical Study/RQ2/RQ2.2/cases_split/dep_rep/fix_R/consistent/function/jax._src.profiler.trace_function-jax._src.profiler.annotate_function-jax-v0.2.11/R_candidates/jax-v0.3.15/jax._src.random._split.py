def _split(key: KeyArray, num: int = 2) -> KeyArray:
  # Alternative to split() to use within random samplers.
  # TODO(frostig): remove and use split() once we always enable_custom_prng
  return key._split(num)
