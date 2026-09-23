  @classmethod
  def from_slice(cls, slc: slice, size: int) -> Slice:
    start, stop, step = slc.indices(size)
    if step < 1:
      raise ValueError(f"slice must have a step >= 1 (found: {step})")
    return cls(start, max((stop - start + step - 1) // step, 0), step)
