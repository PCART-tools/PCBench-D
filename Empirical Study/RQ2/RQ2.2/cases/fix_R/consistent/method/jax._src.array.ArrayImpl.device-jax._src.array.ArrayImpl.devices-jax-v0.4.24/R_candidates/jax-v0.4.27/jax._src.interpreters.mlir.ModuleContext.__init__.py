  def __init__(
      self,
      *,
      backend_or_name: str | xb.XlaBackend | None,
      platforms: Sequence[str],
      axis_context: AxisContext,
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
