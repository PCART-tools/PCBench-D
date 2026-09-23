def _ref_raise_to_shaped(ref_aval: AbstractMemoryRef, weak_type):
  return AbstractMemoryRef(
      jax_core.raise_to_shaped(ref_aval.inner_aval, weak_type),
      ref_aval.memory_space)
