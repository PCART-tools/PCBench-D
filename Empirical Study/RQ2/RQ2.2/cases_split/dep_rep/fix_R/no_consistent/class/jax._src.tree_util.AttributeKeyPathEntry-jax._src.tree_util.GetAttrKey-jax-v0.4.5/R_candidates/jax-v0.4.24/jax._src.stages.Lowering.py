class Lowering(Protocol):
  """Protocol for lowerings, which a user-facing ``Lowered`` encapsulates."""

  def compile(
      self, compiler_options: CompilerOptions | None = None) -> Executable:
    """Compile and return a corresponding ``Executable``."""
    raise NotImplementedError

  def as_text(self, dialect: str | None = None) -> str:
    """A human-readable text representation of this lowering.

    Intended for visualization and debugging purposes. This need not be a valid
    nor reliable serialization. It is relayed directly to external callers.
    """
    raise NotImplementedError

  def compiler_ir(self, dialect: str | None = None) -> Any:
    """An arbitrary object representation of this lowering.

    Intended for debugging purposes. This need not be a valid nor reliable
    serialization. It is relayed directly to external callers, with no
    guarantee on type, structure, or consistency across invocations.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend or
    compiler.

    Args:
      dialect: Optional string specifying a representation dialect
      (e.g. "stablehlo")
    """
    raise NotImplementedError

  def cost_analysis(self) -> Any:
    """A summary of execution cost estimates.

    Intended for visualization and debugging purposes. The object output by
    this is some simple data structure that can easily be printed or serialized
    (e.g. nested dicts, lists, and tuples with numeric leaves). However, its
    structure can be arbitrary: it need not be consistent across versions of JAX
    and jaxlib, or even across invocations. It is relayed directly to external
    callers.

    This function estimates execution cost in the absence of compiler
    optimizations, which may drastically affect the cost. For execution cost
    estimates after optimizations, compile this lowering and see
    ``Compiled.cost_analysis``.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    # TODO(frostig): improve annotation (arbitrary pytree)
    raise NotImplementedError
