def _backend_supports_unbounded_dynamic_shapes(backend: Backend) -> bool:
  return backend.platform == 'iree'
