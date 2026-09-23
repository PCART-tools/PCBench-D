class Lowering(Protocol):
  """Protocol for lowerings, which a user-facing ``Lowered`` encapsulates."""

  def compile(self) -> Executable:
    """Compile and return a corresponding ``Executable``."""
    raise NotImplementedError

  def as_text(self, dialect: Optional[str] = None) -> str:
    """A human-readable text representation of this lowering.

    Intended for visualization and debugging purposes. This need not be a valid
    nor reliable serialization. It is relayed directly to external callers.
    """
    raise NotImplementedError

  def compiler_ir(self, dialect: Optional[str] = None) -> Any:
    """An arbitrary object representation of this lowering.

    Intended for debugging purposes. This need not be a valid nor reliable
    serialization. It is relayed directly to external callers, with no
    guarantee on type, structure, or consistency across invocations.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend or
    compiler.

    Args:
      dialect: Optional string specifying a representation dialect (e.g. "mhlo")
    """
    raise NotImplementedError
