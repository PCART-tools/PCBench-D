class Lowered(Stage):
  """Lowering of a function specialized to argument types and values.

  A lowering is a computation ready for compilation. This class
  carries a lowering together with the remaining information needed to
  later compile and execute it. It also provides a common API for
  querying properties of lowered computations across JAX's various
  lowering paths (:func:`~jax.jit`, :func:`~jax.pmap`, etc.).
  """
  __slots__ = ["args_info", "out_tree", "_lowering", "_no_kwargs"]

  args_info: Any                # PyTree of ArgInfo
  out_tree: tree_util.PyTreeDef
  _lowering: XlaLowering
  _no_kwargs: bool

  def __init__(
      self,
      lowering: XlaLowering,
      args_info,  # PyTree of ArgInfo
      out_tree: tree_util.PyTreeDef,
      no_kwargs: bool = False):
    self._lowering = lowering
    self._no_kwargs = no_kwargs
    self.args_info = args_info
    self.out_tree = out_tree

  @classmethod
  def from_flat_info(cls,
                     lowering: XlaLowering,
                     in_tree: tree_util.PyTreeDef,
                     in_avals,
                     donate_argnums: tuple[int, ...],
                     out_tree: tree_util.PyTreeDef,
                     no_kwargs: bool = False):
    """Initialize from flat info (``in_avals`` etc.) and an input PyTreeDef.

    Args:
      in_tree: The ``PyTreeDef`` of (args, kwargs).
      out_tree: The ``PyTreeDef`` of the outputs.
      no_kwargs: If ``True`` the transformation, and the
        ``Compiled`` returned from this object will not support keyword
        arguments (an error will be raised if some are provided).
    """
    return cls(
        lowering,
        make_args_info(in_tree, in_avals, donate_argnums),
        out_tree,
        no_kwargs=no_kwargs)

  def compile(
      self, compiler_options: CompilerOptions | None = None) -> Compiled:
    """Compile, returning a corresponding ``Compiled`` instance."""
    kw: dict[str, Any] = {"compiler_options": compiler_options}
    return Compiled(
        self._lowering.compile(**kw),  # pytype: disable=wrong-keyword-args
        self.args_info,
        self.out_tree,
        no_kwargs=self._no_kwargs,
    )

  def as_text(self, dialect: str | None = None) -> str:
    """A human-readable text representation of this lowering.

    Intended for visualization and debugging purposes. This need not be a valid
    nor reliable serialization. It is relayed directly to external callers.

    Args:
      dialect: Optional string specifying a lowering dialect (e.g. "stablehlo")
    """
    return self._lowering.as_text(dialect)

  def compiler_ir(self, dialect: str | None = None) -> Any | None:
    """An arbitrary object representation of this lowering.

    Intended for debugging purposes. This is not a valid nor reliable
    serialization. The output has no guarantee of consistency across
    invocations.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.

    Args:
      dialect: Optional string specifying a lowering dialect (e.g. "stablehlo")
    """
    try:
      return self._lowering.compiler_ir(dialect)
    except NotImplementedError:
      return None

  def cost_analysis(self) -> Any | None:
    """A summary of execution cost estimates.

    Intended for visualization and debugging purposes. The object output by
    this is some simple data structure that can easily be printed or serialized
    (e.g. nested dicts, lists, and tuples with numeric leaves). However, its
    structure can be arbitrary: it may be inconsistent across versions of JAX
    and jaxlib, or even across invocations.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.
    """
    # TODO(frostig): improve annotation (basic pytree of arbitrary structure)
    try:
      return self._lowering.cost_analysis()
    except NotImplementedError:
      return None
