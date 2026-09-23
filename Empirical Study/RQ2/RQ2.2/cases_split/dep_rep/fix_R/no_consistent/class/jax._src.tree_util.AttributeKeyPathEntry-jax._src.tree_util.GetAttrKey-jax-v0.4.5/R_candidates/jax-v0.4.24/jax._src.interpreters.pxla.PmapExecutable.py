class PmapExecutable(stages.XlaExecutable):
  __slots__ = ["xla_executable", "_unsafe_call", "build_unsafe_call",
               "fingerprint", "in_avals", "_jaxpr_debug_info",
               "_unloaded_executable"]

  def __init__(self, xla_executable, build_unsafe_call, fingerprint,
               in_avals, jaxpr_debug_info, unloaded_executable):
    self.xla_executable = xla_executable
    self._unsafe_call = None
    self.build_unsafe_call = build_unsafe_call
    self.fingerprint = fingerprint
    self.in_avals = in_avals
    self._jaxpr_debug_info = jaxpr_debug_info
    self._unloaded_executable = unloaded_executable

  @property
  def unsafe_call(self) -> Callable[..., Any]:
    if self._unsafe_call is None:
      self._unsafe_call = self.build_unsafe_call()
    return self._unsafe_call

  # -- stages.XlaExecutable overrides

  def xla_extension_executable(self):
    return self.xla_executable

  @profiler.annotate_function
  def call(self, *args):
    # TODO(frostig): do we need to check sharding and sharded avals?
    arg_avals = map(xla.abstractify, args)
    check_arg_avals_for_call(self.in_avals, arg_avals, self._jaxpr_debug_info)
    return self.unsafe_call(*args)  # pylint: disable=not-callable
