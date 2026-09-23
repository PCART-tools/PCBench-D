class XlaComputation(stages.XlaLowering):
  name: str
  _is_trivial: bool
  _executable: Optional[XlaCompiledComputation]
  _donated_invars: Optional[Sequence[bool]]

  def __init__(self, name: str, hlo, is_trivial: bool,
               donated_invars: Optional[Sequence[bool]],
               in_type: Optional[pe.InputType],
               out_type: Optional[pe.OutputType],
               **compile_args):
    self.name = name
    self._hlo = hlo
    self._is_trivial = is_trivial
    self._donated_invars = donated_invars
    self._in_type = in_type
    self._out_type = out_type
    self._executable = None
    self.compile_args = compile_args

  def is_trivial(self):
    return self._is_trivial

  # -- stages.XlaLowering overrides

  def hlo(self) -> xc.XlaComputation:
    if self.is_trivial():
      raise ValueError("A trivial computation has no HLO")
    if isinstance(self._hlo, xc.XlaComputation):
      return self._hlo
    return xe.mlir.mlir_module_to_xla_computation(
        mlir.module_to_string(self._hlo),
        use_tuple_args=self.compile_args["tuple_args"])

  def mhlo(self) -> ir.Module:
    if self.is_trivial():
      raise ValueError("A trivial computation has no MHLO")
    if isinstance(self._hlo, xc.XlaComputation):
      module_str = xe.mlir.xla_computation_to_mlir_module(self._hlo)
      with mlir.make_ir_context():
        return ir.Module.parse(module_str)
    return self._hlo

  def compile(self) -> XlaCompiledComputation:
    if self._executable is None:
      if self.is_trivial():
        self._executable = XlaCompiledComputation.from_trivial_jaxpr(
            **self.compile_args)
      else:
        self._executable = XlaCompiledComputation.from_xla_computation(
            self.name, self._hlo, self._in_type, self._out_type,
            **self.compile_args)

    return self._executable
