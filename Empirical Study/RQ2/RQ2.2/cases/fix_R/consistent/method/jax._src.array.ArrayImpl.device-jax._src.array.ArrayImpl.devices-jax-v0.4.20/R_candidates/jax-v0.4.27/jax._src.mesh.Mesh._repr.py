  @functools.cached_property
  def _repr(self):
    if self.empty:
      return "Mesh(device_ids=[], axis_names=())"
    return f"Mesh(device_ids={self.device_ids!r}, axis_names={self.axis_names!r})"
