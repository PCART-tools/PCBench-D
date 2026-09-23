  def __init__(self, xla_executable, build_unsafe_call, fingerprint,
               in_avals, jaxpr_debug_info, unloaded_executable):
    self.xla_executable = xla_executable
    self._unsafe_call = None
    self.build_unsafe_call = build_unsafe_call
    self.fingerprint = fingerprint
    self.in_avals = in_avals
    self._jaxpr_debug_info = jaxpr_debug_info
    self._unloaded_executable = unloaded_executable
