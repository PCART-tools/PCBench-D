def _make_aval(obj: object) -> jax_core.AbstractValue:
  if isinstance(obj, MemoryRef):
    return obj.get_aval()
  if isinstance(obj, SemaphoreType):
    return obj.get_aval()
  raise ValueError(f"No registered conversion for {type(obj)}. "
                   "Only VMEM and SemaphoreType are supported.")
