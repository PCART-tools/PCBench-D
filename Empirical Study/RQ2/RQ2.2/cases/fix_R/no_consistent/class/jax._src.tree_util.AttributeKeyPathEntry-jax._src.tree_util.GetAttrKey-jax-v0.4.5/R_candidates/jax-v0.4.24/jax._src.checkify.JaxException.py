class JaxException(Exception):
  """Python exception which can contain an error message with JAX run-time info."""

  def __init__(self, traceback_info):
    self.traceback_info = traceback_info
    # TODO(lenamartens): re-enable tracebacks when they don't leak tracers.
    # self.with_traceback(self.traceback_info)

  def __init_subclass__(cls):
    jtu.register_pytree_node_class(cls)

  def tree_flatten(self):
    return ([], self.traceback_info)

  @classmethod
  def tree_unflatten(cls, metadata, payload):
    del payload
    return cls(metadata)

  def get_effect_type(self) -> ErrorEffect:
    raise NotImplementedError
