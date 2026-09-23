  def as_text(self, dialect: str | None = None) -> str:
    """A human-readable text representation of this lowering.

    Intended for visualization and debugging purposes. This need not be a valid
    nor reliable serialization. It is relayed directly to external callers.

    Args:
      dialect: Optional string specifying a lowering dialect (e.g. "stablehlo")
    """
    return self._lowering.as_text(dialect)
