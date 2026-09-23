def process_count(backend: Optional[Union[str, XlaBackend]] = None) -> int:
  """Returns the number of JAX processes associated with the backend."""
  return max(d.process_index for d in devices(backend)) + 1
