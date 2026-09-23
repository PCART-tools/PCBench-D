  def filter(self,
             device_under_test: str,
             *,
             include_jax_unimpl: bool = False,
             one_containing: str | None = None) -> bool:
    if not include_jax_unimpl:
      if any(
          device_under_test in l.devices
          for l in self.jax_unimplemented
          if l.filter(device=device_under_test, dtype=self.dtype)
      ):
        return False

    if one_containing is not None and one_containing not in self.fullname:
      return False
    return True
