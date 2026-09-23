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
