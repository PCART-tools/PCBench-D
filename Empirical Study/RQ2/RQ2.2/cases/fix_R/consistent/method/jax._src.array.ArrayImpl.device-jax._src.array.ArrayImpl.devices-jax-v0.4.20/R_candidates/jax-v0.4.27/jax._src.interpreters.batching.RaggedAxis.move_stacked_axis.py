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
