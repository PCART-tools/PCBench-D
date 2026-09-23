class PmapComputation(stages.XlaLowering):
  _hlo: ir.Module
  _executable: PmapExecutable | None

  def __init__(self, hlo: ir.Module, **compile_args):
    self._executable = None
    self._hlo = hlo
    self.compile_args = compile_args

  # -- stages.XlaLowering overrides

  def stablehlo(self) -> ir.Module:
    return self._hlo

  @profiler.annotate_function
  def compile(self, compiler_options=None) -> PmapExecutable:
    if self._executable is None or compiler_options is not None:
      executable = UnloadedPmapExecutable.from_hlo(
          self._hlo, **self.compile_args,
          compiler_options=compiler_options)
      if compiler_options is None:
        self._executable = executable
      return executable
    return self._executable
