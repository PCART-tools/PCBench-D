def _to_xla_layout(layout: XLACompatibleLayout | None | LayoutRequest) -> str | None:
  if layout is None:
    return "default"
  if isinstance(layout, LayoutRequest):
    return "auto"
  return layout._to_xla_layout()
