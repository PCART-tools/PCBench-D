@dataclasses.dataclass(frozen=True)
class RaggedAxis:
  stacked_axis: int
  # For each axis, we store its index and the corresponding segment lengths.
  # For example, the jumble i:(Fin 3) => f32[lens1.i, 7, lens2.i]
  # would be represented with ragged_axes = [(1, lens1), (3, lens2)]
  ragged_axes: tuple[tuple[int, Any], ...]

  @property
  def size(self):
    # TODO(mattjj, axch): All the segment lengths arrays better be the
    # same length!
    return len(self.ragged_axes[0][1])

  def move_stacked_axis(self: RaggedAxis, dst: int) -> RaggedAxis:
    # Assumes that all stored and incoming axes are already canonicalized
    def move_axis(ax):
      if self.stacked_axis > ax and ax >= dst:
        return ax + 1
      if self.stacked_axis < ax and ax <= dst:
        return ax - 1
      return ax
    new_axes = tuple((move_axis(ax), sizes) for ax, sizes in self.ragged_axes)
    return RaggedAxis(dst, new_axes)
