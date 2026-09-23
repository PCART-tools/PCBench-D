class MeshComputation(stages.XlaLowering):
  _hlo: ir.Module | None
  _executable: MeshExecutable | None

  def __init__(self, name: str, hlo: ir.Module | None,
               donated_invars: Sequence[bool], **compile_args):
    self._name = name
    self._hlo = hlo
    self._donated_invars = donated_invars
    self.compile_args = compile_args
    self._executable = None

  # -- stages.XlaLowering overrides

  def stablehlo(self) -> ir.Module:
    return self._hlo

  def compile(self, compiler_options=None) -> MeshExecutable:
    if self._executable is None or compiler_options is not None:
      executable = UnloadedMeshExecutable.from_hlo(
          self._name, self._hlo, **self.compile_args,
          compiler_options=compiler_options)
      if compiler_options is None:
        self._executable = executable
      return executable
    return self._executable

  def cost_analysis(self) -> dict[str, float]:
    backend = self.compile_args["backend"]
    if xb.using_pjrt_c_api(backend):
      raise NotImplementedError(
          "Lowered.cost_analysis not implemented on platform "
          f"'{backend.platform}'. Use compile().cost_analysis() for "
          "post-compilation cost estimates.")
    return xe.hlo_module_cost_analysis(backend, self.hlo().as_hlo_module())
