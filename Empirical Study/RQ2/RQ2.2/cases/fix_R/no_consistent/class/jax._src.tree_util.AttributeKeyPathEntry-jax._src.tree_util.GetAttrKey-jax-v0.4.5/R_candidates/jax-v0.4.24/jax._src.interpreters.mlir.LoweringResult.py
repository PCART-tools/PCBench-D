class LoweringResult(NamedTuple):
  module: ir.Module
  keepalive: Any | None
  host_callbacks: list[Any]
  shape_poly_state: ShapePolyLoweringState
