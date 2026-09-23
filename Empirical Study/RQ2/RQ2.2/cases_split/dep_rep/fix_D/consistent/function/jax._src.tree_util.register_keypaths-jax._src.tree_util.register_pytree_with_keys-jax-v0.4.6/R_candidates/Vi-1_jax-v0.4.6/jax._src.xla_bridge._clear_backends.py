def _clear_backends():
  global _backends
  global _backends_errors
  global _default_backend

  logger.info("Clearing JAX backend caches.")
  with _backend_lock:
    _backends = {}
    _backends_errors = {}
    _default_backend = None

  get_backend.cache_clear()
