  @property
  def size(self):
    # TODO(mattjj, axch): All the segment lengths arrays better be the
    # same length!
    return len(self.ragged_axes[0][1])
