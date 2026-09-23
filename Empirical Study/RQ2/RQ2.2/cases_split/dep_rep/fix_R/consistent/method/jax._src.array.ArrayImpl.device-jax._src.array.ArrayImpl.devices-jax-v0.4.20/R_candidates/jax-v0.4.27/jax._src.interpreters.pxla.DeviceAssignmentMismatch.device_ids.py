  @property
  def device_ids(self) -> Sequence[int]:
    return [d.id for d in self.da]
