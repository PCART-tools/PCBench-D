  @property
  def backend(self) -> xb.XlaBackend:
    # TODO(necula): clean the use of backend and backend_or_name vs. platforms
    if len(self.platforms) > 1:
      raise NotImplementedError(
        "accessing .backend in multi-lowering setting. This can occur when "
        "lowering a primitive that has not been adapted to multi-platform "
        "lowering")
    if self.backend_or_name is None or isinstance(self.backend_or_name, str):
      return xb.get_backend(self.backend_or_name)
    return self.backend_or_name
