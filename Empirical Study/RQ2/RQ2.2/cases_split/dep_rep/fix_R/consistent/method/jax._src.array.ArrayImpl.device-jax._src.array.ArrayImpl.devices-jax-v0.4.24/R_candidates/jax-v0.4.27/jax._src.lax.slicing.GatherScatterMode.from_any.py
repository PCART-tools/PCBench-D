  @staticmethod
  def from_any(s: str | GatherScatterMode | None):
    if isinstance(s, GatherScatterMode):
      return s
    if s == "clip":
      return GatherScatterMode.CLIP
    if s is None or s == "fill" or s == "drop":
      return GatherScatterMode.FILL_OR_DROP
    if s == "promise_in_bounds":
      return GatherScatterMode.PROMISE_IN_BOUNDS
    else:
      raise ValueError(f'Unknown gather mode "{s}"')
