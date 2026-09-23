@dataclasses.dataclass
class ModuleContext:
  """Module-wide context information for MLIR lowering."""
  context: ir.Context
  module: ir.Module
  ip: ir.InsertionPoint
  symbol_table: ir.SymbolTable
  backend_or_name: str | xb.XlaBackend | None
  platforms: Sequence[str]
  axis_context: AxisContext
  name_stack: source_info_util.NameStack
  keepalives: list[Any]
  channel_iterator: Iterator[int]
  host_callbacks: list[Any]
  # Keep state for the lowering of shape polymorphism
  shape_poly_state: ShapePolyLoweringState

  # Cached primitive lowerings.
  cached_primitive_lowerings: dict[Any, func_dialect.FuncOp]

  # Cached traceback infromation.
  traceback_caches: TracebackCaches

  lowering_parameters: LoweringParameters

  @property
  def axis_env(self) -> sharding_impls.AxisEnv:
    return self.axis_context.axis_env

  def __init__(
      self,
      *,
      backend_or_name: str | xb.XlaBackend | None,
      platforms: Sequence[str],
      axis_context: AxisContext,
      name_stack: source_info_util.NameStack,
      keepalives: list[Any],
      channel_iterator: Iterator[int],
      host_callbacks: list[Any],
      lowering_parameters: LoweringParameters,
      context: ir.Context | None = None,
      module: ir.Module | None = None,
      ip: ir.InsertionPoint | None = None,
      symbol_table: ir.SymbolTable | None = None,
      cached_primitive_lowerings: None | (dict[Any,
                                                func_dialect.FuncOp]) = None,
      traceback_caches: None | TracebackCaches = None,
      shape_poly_state = None):

    self.context = context or make_ir_context()
    self.module = module or ir.Module.create(loc=ir.Location.unknown(self.context))
    self.ip = ip or ir.InsertionPoint(self.module.body)
    self.symbol_table = symbol_table or ir.SymbolTable(self.module.operation)
    self.backend_or_name = backend_or_name
    self.platforms = platforms
    self.axis_context = axis_context
    self.name_stack = name_stack
    self.cached_primitive_lowerings = ({} if cached_primitive_lowerings is None
                                       else cached_primitive_lowerings)
    self.traceback_caches = (TracebackCaches() if traceback_caches is None
                             else traceback_caches)
    self.channel_iterator = channel_iterator
    self.keepalives = keepalives
    self.host_callbacks = host_callbacks
    self.shape_poly_state = (
      shape_poly_state or ShapePolyLoweringState((), tuple(platforms)))
    self.lowering_parameters = lowering_parameters

  @property
  def backend(self) -> xb.XlaBackend:
    # TODO(necula): clean the use of backend and backend_or_name vs. platforms
    if len(self.platforms) > 1:
      raise NotImplementedError(
        "accessing .backend in multi-lowering setting. This can occur when "
        "lowering a primitive that has not been adapted to multi-platform "
        "lowering")
    if self.backend_or_name is None or isinstance(self.backend_or_name, str):
      return xb.get_backend(self.backend_or_name)
    return self.backend_or_name

  def new_channel(self) -> int:
    return next(self.channel_iterator)

  # Adds an IFRT host callback object to the context. A reference to these
  # callbacks will be provided to IFRT during compilation so it can do things
  # like serialize them and keep them alive.
  def add_host_callback(self, host_callback: Any) -> None:
    self.host_callbacks.append(host_callback)

  # Keeps a value alive as long as the Python executable is alive.
  # TODO(phawkins): this feature is problematic, because you almost certainly
  # want to keep alive values as long as the underlying runtime executable is
  # still alive/executing. The Python executable object may have a shorter
  # lifetime, so it's highly likely any caller of this method is buggy.
  def add_keepalive(self, keepalive: Any) -> None:
    self.keepalives.append(keepalive)

  def replace(self, **kw): return dataclasses.replace(self, **kw)
