  def full_raise(self, val) -> TracerType:
    if not isinstance(val, Tracer):
      # This check is only applied to non-Tracers, because the hasattr() is
      # expensive (Tracer.__getattr__) in the common case that val is a Tracer.
      if hasattr(val, "dimension_as_value"):  # Used for shape_poly._DimExpr
        val = val.dimension_as_value()
        if not isinstance(val, Tracer):
          return self.pure(val)
      else:
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
