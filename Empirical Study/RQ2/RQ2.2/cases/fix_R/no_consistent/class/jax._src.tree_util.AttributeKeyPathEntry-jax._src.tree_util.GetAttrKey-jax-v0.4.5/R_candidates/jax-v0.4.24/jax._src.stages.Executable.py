class Executable(Protocol):
  """Protocol for executables, which a user-facing ``Compiled`` encapsulates."""

  def call(self, *args_flat) -> Sequence[Any]:
    """Execute on the flat list of arguments, returning flat outputs."""
    # TODO(frostig): improve annotation (sequences of arrays/buffers)
    raise NotImplementedError

  def input_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    """Flat sequence of input shardings.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    raise NotImplementedError

  def output_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    """Flat sequence of output shardings.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    raise NotImplementedError

  # Layouts are exposed via jax.experimental.layouts
  # TODO(frostig,yashkatariya): expose here when no longer experimental.
  def _input_layouts(self):
    raise NotImplementedError

  def _output_layouts(self):
    raise NotImplementedError

  def as_text(self) -> str:
    """A human-readable text representation of this executable.

    Intended for visualization and debugging purposes. This need not be a valid
    nor reliable serialization. It is relayed directly to external callers.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
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

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    # TODO(frostig): improve annotation (arbitrary pytree)
    raise NotImplementedError

  def memory_analysis(self) -> Any:
    """A summary of estimated memory requirements.

    Intended for visualization and debugging purposes. The object output by
    this is some simple data structure that can easily be printed or serialized
    (e.g. nested dicts, lists, and tuples with numeric leaves). However, its
    structure can be arbitrary: it need not be consistent across versions of JAX
    and jaxlib, or even across invocations. It is relayed directly to external
    callers.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend,
    compiler, or runtime.
    """
    # TODO(frostig): improve annotation (arbitrary pytree)
    raise NotImplementedError

  def runtime_executable(self) -> Any:
    """An arbitrary object representation of this executable.

    Intended for debugging purposes. This need not be a valid nor reliable
    serialization. It is relayed directly to external callers, with no
    guarantee on type, structure, or consistency across invocations.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend or
    compiler.
    """
    raise NotImplementedError

  def create_cpp_call(self, no_kwargs, in_tree, out_tree) -> Any:
    """Optionally constructs a fast c++ dispatcher."""
    return None
