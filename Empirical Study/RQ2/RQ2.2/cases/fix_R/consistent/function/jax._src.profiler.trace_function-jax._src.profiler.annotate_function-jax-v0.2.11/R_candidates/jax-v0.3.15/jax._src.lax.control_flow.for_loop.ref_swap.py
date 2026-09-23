def ref_swap(ref: Ref, idx: Tuple[int], value: Array) -> Array:
  """Sets a `Ref`'s value and returns the original value."""
  idx = map(jnp.int32, idx)
  return swap_p.bind(ref, value, *idx)
