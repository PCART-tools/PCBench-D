def _binary_replace(replace_bit, original_dict, new_dict, keys=None):
  if keys is None:
    keys = new_dict.keys()
  out = dict()
  for key in keys:
    out[key] = jnp.where(replace_bit, new_dict[key], original_dict[key])
  return out
