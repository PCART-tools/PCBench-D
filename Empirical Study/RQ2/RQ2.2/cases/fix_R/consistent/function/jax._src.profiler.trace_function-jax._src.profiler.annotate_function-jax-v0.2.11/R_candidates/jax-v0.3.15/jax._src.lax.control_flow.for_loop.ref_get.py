def ref_get(ref: Ref, idx: Tuple[int]) -> Array:
  """Reads a value from a `Ref`, a.k.a. value <- ref[idx]."""
  idx = map(jnp.int32, idx)
  return get_p.bind(ref, *idx)
