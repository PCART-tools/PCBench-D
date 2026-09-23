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
