def register_backend_factory(name, factory, *, priority=0):
  with _backend_lock:
    if name in _backends:
      raise RuntimeError(f"Backend {name} already initialized")
  _backend_factories[name] = (factory, priority)
