@lru_cache
def process_count(
    backend: Optional[Union[str, xla_client.Client]] = None
) -> int:
  """Returns the number of JAX processes associated with the backend."""
  return max(d.process_index for d in devices(backend)) + 1
