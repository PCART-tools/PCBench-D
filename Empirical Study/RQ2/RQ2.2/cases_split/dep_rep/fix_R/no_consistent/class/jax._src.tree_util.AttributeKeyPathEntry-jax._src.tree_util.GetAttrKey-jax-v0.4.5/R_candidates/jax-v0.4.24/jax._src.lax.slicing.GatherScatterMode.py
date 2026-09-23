class GatherScatterMode(enum.Enum):
  """
  Describes how to handle out-of-bounds indices in a gather or scatter.

  Possible values are:

  CLIP:
    Indices will be clamped to the nearest in-range value, i.e., such that the
    entire window to be gathered is in-range.
  FILL_OR_DROP:
    If any part of a gathered window is out of bounds, the entire window
    that is returned, even those elements that were otherwise in-bounds, will be
    filled with a constant.
    If any part of a scattered window is out of bounds, the entire window
    will be discarded.
  PROMISE_IN_BOUNDS:
    The user promises that indices are in bounds. No additional checking will be
    performed. In practice, with the current XLA  implementation this means
    that, out-of-bounds gathers will be clamped but out-of-bounds scatters will
    be discarded. Gradients will not be correct if indices are out-of-bounds.
  """
  CLIP = enum.auto()
  FILL_OR_DROP = enum.auto()
  PROMISE_IN_BOUNDS = enum.auto()

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
