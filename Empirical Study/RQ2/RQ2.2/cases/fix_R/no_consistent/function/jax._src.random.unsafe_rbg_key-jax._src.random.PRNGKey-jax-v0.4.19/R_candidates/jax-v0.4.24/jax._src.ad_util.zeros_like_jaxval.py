def zeros_like_jaxval(val):
  return zeros_like_aval(core.raise_to_shaped(core.get_aval(val)))
