class AllArgsInfo(NamedTuple):
  """Avals, shardings, layouts and debug_info for all arguments prior to DCE."""
  in_avals: Sequence[core.ShapedArray]
  in_shardings: Any
  debug_info: core.JaxprDebugInfo | None
