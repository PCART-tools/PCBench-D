  def __init__(self, xla_executable, name, backend, in_handler: InputsHandler,
               out_handler: ResultsHandler,
               unordered_effects: list[core.Effect],
               ordered_effects: list[core.Effect], keepalive: Any,
               has_host_callbacks: bool, kept_var_idx: set[int],
               mut: MutationData | None):
    self.xla_executable = xla_executable
    self.name = name
    self.backend = backend
    self.in_handler = in_handler
    self.out_handler = out_handler
    self.has_unordered_effects = bool(unordered_effects)
    self.ordered_effects = ordered_effects
    self._local_devices = self.xla_executable.local_devices()
    self.keepalive = keepalive
    self.has_host_callbacks = has_host_callbacks
    self.kept_var_idx = kept_var_idx
    self.mut = mut
