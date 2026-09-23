def map_bind(primitive: MapPrimitive, fun, *args, **params):
  map_bind_continuation, top_trace, fun, tracers, params = (
      map_bind_with_continuation(primitive, fun, *args, **params))
  return map_bind_continuation(
      primitive.process(top_trace, fun, tracers, params))
