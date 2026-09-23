class XlaLowering(Lowering):
  """Adapts our various internal XLA-backed computations into a ``Lowering``."""

  compile_args: dict[str, Any]

  def hlo(self) -> xc.XlaComputation:
    """Return an HLO representation of this computation."""
    return xla_extension.mlir.mlir_module_to_xla_computation(
        mlir.module_to_string(self.stablehlo()),
        use_tuple_args=self.compile_args["tuple_args"])

  def mhlo(self) -> ir.Module:
    """Return an MHLO representation of this computation."""
    warnings.warn(
        "mhlo support is deprecated and will be removed "
        "from a future release of JAX. Use stablehlo instead.",
        DeprecationWarning,
    )
    module_str = xla_extension.mlir.stablehlo_to_mhlo(
        mlir.module_to_bytecode(self.stablehlo()))
    with self.stablehlo().context:
      return ir.Module.parse(module_str)

  def stablehlo(self) -> ir.Module:
    """Return a StableHLO representation of this computation."""
    raise NotImplementedError("must override")

  def compile(
      self, compiler_options: CompilerOptions | None = None) -> Executable:
    raise NotImplementedError("must override")

  def as_text(self, dialect: str | None = None) -> str:
    if dialect is None:
      dialect = "stablehlo"
    if dialect == "mhlo":
      return str(self.mhlo())
    elif dialect == "stablehlo":
      return str(self.stablehlo())
    elif dialect == "hlo":
      return self.hlo().as_hlo_text()
    else:
      raise ValueError(f"unknown dialect: {dialect}")

  def compiler_ir(self, dialect: str | None = None) -> Any:
    if dialect is None:
      dialect = "stablehlo"
    if dialect == "mhlo":
      return self.mhlo()
    elif dialect == "stablehlo":
      return self.stablehlo()
    elif dialect == "hlo":
      return self.hlo()
    else:
      raise ValueError(f"unknown dialect: {dialect}")

  def cost_analysis(self) -> dict[str, float]:
    raise NotImplementedError("must override")
