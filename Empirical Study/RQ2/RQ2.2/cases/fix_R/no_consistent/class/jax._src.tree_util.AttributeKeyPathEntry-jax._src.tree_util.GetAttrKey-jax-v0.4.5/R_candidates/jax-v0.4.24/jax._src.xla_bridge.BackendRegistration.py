@dataclasses.dataclass
class BackendRegistration:
  factory: BackendFactory

  # Priority of this backend when choosing a default backend. Higher = more
  # preferred.
  priority: int

  # If this backend fails to initialize, should we log a user-visible warning?
  # For plugins (e.g., TPU) we usually want a visible failure, because why
  # install a plugin if you don't intend it to be used?
  fail_quietly: bool = False

  # Is this plugin experimental? If a plugin is deemed experimental, we issue
  # a warning when it is initialized. This is mostly to set user expectations
  # correctly: we don't want users to think that JAX is buggy because of a
  # a buggy plugin.
  experimental: bool = False
