class Trace(Generic[TracerType]):
  __slots__ = ['main', 'level', 'sublevel']

  main: MainTrace
  level: int
  sublevel: Sublevel

  def __init__(self, main: MainTrace, sublevel: Sublevel) -> None:
    self.main = main
    self.level = main.level
    self.sublevel = sublevel

  def full_raise(self, val) -> TracerType:
    if hasattr(val, "dimension_as_value"):  # Used for shape_poly._DimPolynomial
      val = val.dimension_as_value()
    if not isinstance(val, Tracer):
      return self.pure(val)
    val._assert_live()
    level = self.level
    sublevel = self.sublevel
    if val._trace.main is self.main:
      if val._trace.sublevel == sublevel:
        return cast(TracerType, val)
      elif val._trace.sublevel < sublevel:
        return self.sublift(val)
      else:
        raise escaped_tracer_error(
            val, f"Can't lift sublevels {val._trace.sublevel} to {sublevel}")
    elif val._trace.level < level:
      if val._trace.sublevel > sublevel:
        raise escaped_tracer_error(
            val, f"Incompatible sublevel: {val._trace}, {(level, sublevel)}")
      return self.lift(val)
    elif val._trace.level > level:
      raise escaped_tracer_error(
          val, f"Can't lift level {val} to {self}")
    else:  # val._trace.level == self.level:
      raise escaped_tracer_error(
          val, f"Different traces at same level: {val}, {self}")

  def pure(self, val) -> TracerType:
    raise NotImplementedError("must override")

  def lift(self, tracer) -> TracerType:
    raise NotImplementedError("must override")

  def sublift(self, tracer) -> TracerType:
    raise NotImplementedError("must override")

  def process_primitive(self, primitive, tracers, params):
    raise NotImplementedError("must override")

  def __repr__(self):
    return '{}(level={}/{})'.format(
        self.__class__.__name__, self.level, self.sublevel)

  def process_call(self, call_primitive, f, tracers, params):
    msg = (f"{type(self)} must override process_call to handle call-like "
           "primitives")
    raise NotImplementedError(msg)

  def process_map(self, map_primitive, f, tracers, params):
    msg = (f"{type(self)} must override process_map to handle map-like "
           "primitives")
    raise NotImplementedError(msg)

  def process_custom_jvp_call(self, primitive, fun, jvp, tracers, *,
                              symbolic_zeros):
    msg = (f"{type(self)} must override process_custom_jvp_call "
           "to handle custom_jvp primitives")
    raise NotImplementedError(msg)

  def process_custom_transpose(self, prim, call, tracers, **params):
    msg = (f"{type(self)} must override process_custom_transpose "
           "to handle custom_transpose_call primitives")
    raise NotImplementedError(msg)

  def process_custom_vjp_call(self, primitive, fun, fwd, bwd, tracers,
                              out_trees, symbolic_zeros):
    msg = (f"{type(self)} must override process_custom_vjp_call "
           "to handle custom_vjp primitives")
    raise NotImplementedError(msg)
