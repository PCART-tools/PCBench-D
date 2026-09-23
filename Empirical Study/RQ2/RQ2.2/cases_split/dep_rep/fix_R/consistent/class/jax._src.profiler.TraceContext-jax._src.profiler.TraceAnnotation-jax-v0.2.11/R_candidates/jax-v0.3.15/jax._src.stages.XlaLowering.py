class XlaLowering(Lowering):
  """Adapts our various internal XLA-backed computations into a ``Lowering``."""

  def hlo(self) -> xc.XlaComputation:
    """Return an HLO representation of this computation."""
    raise NotImplementedError("must override")

  def mhlo(self) -> mlir.ir.Module:
    """Return an MHLO representation of this computation."""
    raise NotImplementedError("must override")

  def compile(self) -> Executable:
    raise NotImplementedError("must override")

  def as_text(self, dialect: Optional[str] = None) -> str:
    if dialect is None or dialect == "mhlo":
      return str(self.mhlo())
    elif dialect == "hlo":
      return self.hlo().as_hlo_text()
    else:
      raise ValueError(f"unknown dialect: {dialect}")

  def compiler_ir(self, dialect: Optional[str] = None) -> Any:
    if dialect is None or dialect == "mhlo":
      return self.mhlo()
    elif dialect == "hlo":
      return self.hlo()
    else:
      raise ValueError(f"unknown dialect: {dialect}")
